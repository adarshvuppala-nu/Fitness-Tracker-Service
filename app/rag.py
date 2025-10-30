"""RAG Pipeline with FAISS for Fitness Knowledge Base"""

import os
from typing import List, Dict, Optional
import pickle
from pathlib import Path

from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

from app.core.config import settings


FITNESS_KNOWLEDGE_BASE = """
# Comprehensive Fitness & Wellness Knowledge Base

 Workout Types and Benefits

# Cardiovascular Exercise
Running: Improves cardiovascular health, burns 300-600 calories per hour. Ideal duration: 20-60 minutes.
Best for: Weight loss, endurance, heart health.
Recommended frequency: 3-5 times per week.

Cycling: Low-impact cardio, burns 400-750 calories per hour. Great for joint health.
Best for: Endurance, leg strength, recovery days.
Recommended frequency: 3-5 times per week.

Swimming: Full-body workout, burns 400-700 calories per hour. Excellent for injury rehabilitation.
Best for: Total body conditioning, low-impact training.
Recommended frequency: 2-4 times per week.

HIIT (High-Intensity Interval Training): Burns 500-800 calories in 30 minutes. Boosts metabolism for 24-48 hours post-workout.
Best for: Fast fat loss, time efficiency, metabolic conditioning.
Recommended frequency: 2-3 times per week (requires recovery).

# Strength Training
Weight Training: Builds muscle mass, increases metabolic rate, burns 200-400 calories per hour.
Best for: Muscle building, bone density, strength gains.
Recommended frequency: 3-5 times per week (split by muscle groups).

Bodyweight Exercises: Push-ups, pull-ups, squats. Improves functional strength.
Best for: Beginners, home workouts, functional fitness.
Recommended frequency: 3-4 times per week.

Powerlifting: Focuses on squat, bench press, deadlift. Maximum strength development.
Best for: Absolute strength, power development.
Recommended frequency: 3-4 times per week.

# Flexibility & Recovery
Yoga: Improves flexibility, reduces stress, burns 150-300 calories per hour.
Best for: Flexibility, stress relief, mindfulness.
Recommended frequency: 2-4 times per week.

Pilates: Core strengthening, posture improvement, burns 200-350 calories per hour.
Best for: Core stability, injury prevention, posture.
Recommended frequency: 2-3 times per week.

Stretching: Essential for injury prevention and recovery. 10-15 minutes daily recommended.

 Nutrition Guidelines

# Macronutrients
Protein: 1.6-2.2g per kg bodyweight for muscle building. Sources: chicken, fish, eggs, tofu, legumes.
Essential for: Muscle repair, satiety, metabolic health.

Carbohydrates: 3-5g per kg bodyweight for active individuals. Sources: rice, oats, sweet potato, fruits.
Essential for: Energy, workout performance, recovery.

Fats: 0.8-1.2g per kg bodyweight. Sources: avocado, nuts, olive oil, fatty fish.
Essential for: Hormone production, vitamin absorption, brain health.

# Hydration
Water intake: 30-40ml per kg bodyweight daily. More during intense training.
Electrolytes: Important for workouts longer than 60 minutes.
Pre-workout: Drink 400-600ml water 2-3 hours before exercise.
During workout: 150-250ml every 15-20 minutes for intense sessions.
Post-workout: Replace 150% of fluid lost through sweat.

# Meal Timing
Pre-workout (2-3 hours before): Balanced meal with carbs and protein.
Pre-workout (30-60 minutes before): Light snack, easily digestible carbs.
Post-workout (within 2 hours): Protein and carbs for recovery.
Daily: 4-6 smaller meals or 3 larger meals, based on preference.

 Fitness Goals and Strategies

# Weight Loss
Caloric deficit: 300-500 calories below maintenance for sustainable loss.
Expected loss: 0.5-1kg per week is healthy and sustainable.
Training: Combine cardio (3-5x/week) with strength training (3x/week).
Nutrition: High protein (2.2g/kg), moderate carbs, healthy fats.

# Muscle Building (Hypertrophy)
Caloric surplus: 200-300 calories above maintenance.
Expected gain: 0.25-0.5kg per week (minimizing fat gain).
Training: Progressive overload, 8-12 reps, 3-5 sets, 3-5x/week.
Nutrition: High protein (2.0g/kg), sufficient carbs for energy.

# Endurance Training
Focus: Gradually increase workout duration and intensity.
Training: 60-80% max heart rate for aerobic base building.
Long runs/rides: 1-2x per week at lower intensity.
Nutrition: Higher carbohydrate intake (5-7g/kg bodyweight).

# Strength Gains
Focus: Progressive overload with heavy weights (80-95% 1RM).
Training: Low reps (3-6), high sets (4-6), longer rest periods (3-5 min).
Frequency: 3-4x per week with adequate recovery.
Nutrition: Sufficient calories and protein (1.8-2.2g/kg).

 Recovery and Rest

# Sleep
Optimal duration: 7-9 hours per night for adults.
Recovery benefits: Muscle repair, hormone regulation, cognitive function.
Sleep quality: Dark room, cool temperature (18-20°C), consistent schedule.

# Active Recovery
Light cardio: Walking, cycling at low intensity.
Yoga or stretching: Improves flexibility and blood flow.
Frequency: 1-2 sessions per week between intense workouts.

# Rest Days
Importance: Prevents overtraining, reduces injury risk, allows adaptation.
Recommendation: At least 1-2 full rest days per week.

# Injury Prevention
Warm-up: 5-10 minutes light cardio + dynamic stretching.
Cool-down: 5-10 minutes light activity + static stretching.
Form: Proper technique is more important than weight.
Progression: Increase intensity/volume gradually (10% rule).

 Common Workout Metrics

# Heart Rate Zones
Zone 1 (50-60% max HR): Very light, recovery
Zone 2 (60-70% max HR): Light, fat burning
Zone 3 (70-80% max HR): Moderate, aerobic fitness
Zone 4 (80-90% max HR): Hard, lactate threshold
Zone 5 (90-100% max HR): Maximum, anaerobic

Max Heart Rate estimation: 220 - age

# Caloric Burn Estimates
Walking (4 km/h): 200-300 cal/hour
Running (8 km/h): 400-600 cal/hour
Cycling (20 km/h): 400-600 cal/hour
Swimming: 400-700 cal/hour
Weight training: 200-400 cal/hour
HIIT: 500-800 cal/hour
Yoga: 150-300 cal/hour

Note: Actual burn varies by weight, intensity, fitness level.

 Progress Tracking

# Key Metrics to Monitor
Body weight: Weekly weigh-ins, same time/conditions
Body composition: Body fat percentage, muscle mass
Measurements: Waist, hips, chest, arms, thighs
Performance: Strength gains, endurance improvements, workout duration
Photos: Monthly progress pictures
Energy levels: Subjective rating of daily energy
Sleep quality: Duration and restfulness
Stress levels: Impact on training and recovery

# Goal Setting Framework (SMART)
Specific: Clear, well-defined objectives
Measurable: Quantifiable metrics for progress
Achievable: Realistic based on current fitness level
Relevant: Aligned with personal health priorities
Time-bound: Set deadlines for accountability

Examples of SMART goals:
- "Lose 5kg in 10 weeks through 4x cardio/week and caloric deficit"
- "Increase bench press 1RM from 80kg to 90kg in 8 weeks"
- "Run 5km in under 25 minutes within 12 weeks"
- "Attend yoga class 2x per week for 6 weeks to improve flexibility"

 Supplements (Optional)

# Evidence-Based Supplements
Protein powder: Convenient protein source, 20-30g per serving
Creatine: 3-5g daily improves strength and power output
Caffeine: 3-6mg/kg bodyweight pre-workout for performance
Omega-3: 1-3g daily for inflammation and recovery
Vitamin D: If deficient, supports bone health and immunity
Multivitamin: Insurance against dietary gaps

Note: Whole foods should be the primary nutrition source.

 Mental Health & Fitness

# Exercise Benefits for Mental Health
Reduces anxiety and depression symptoms
Improves mood through endorphin release
Enhances cognitive function and memory
Boosts self-esteem and confidence
Promotes better sleep quality

# Mind-Body Connection
Meditation: 10-20 minutes daily reduces stress
Mindful exercise: Yoga, tai chi for mental clarity
Breathing techniques: 4-7-8 breathing for relaxation
Visualization: Mental rehearsal improves performance

# Avoiding Burnout
Listen to your body: Rest when needed
Variety: Mix different workout types
Social support: Train with friends or groups
Realistic expectations: Progress takes time
Enjoy the process: Find activities you love

 Special Populations

# Beginners
Start slowly: 2-3 workouts per week
Focus on form: Master technique before adding weight
Build base: Cardio and bodyweight exercises
Seek guidance: Consider working with a trainer initially

# Advanced Athletes
Periodization: Structured training phases (hypertrophy, strength, power, deload)
Sport-specific: Tailor training to performance goals
Recovery: Prioritize sleep, nutrition, stress management
Testing: Regular assessment of progress (1RM tests, time trials)

# Older Adults (50+)
Resistance training: Crucial for maintaining muscle mass and bone density
Balance exercises: Prevent falls and maintain functional fitness
Low-impact options: Swimming, cycling, walking
Flexibility: Daily stretching and mobility work

# Pregnancy & Postpartum
Consult healthcare provider before starting/continuing exercise
Avoid: High-impact, contact sports, exercises lying flat on back (after 1st trimester)
Focus on: Core stability, pelvic floor exercises, moderate cardio
Postpartum: Gradual return to exercise after medical clearance
"""

class FitnessRAG:
    """
    Retrieval-Augmented Generation system for fitness knowledge.

    Provides semantic search over fitness documents to augment LLM responses
    with accurate, grounded information.
    """

    def __init__(self, persist_directory: str = "./data/vectorstore"):
        """
        Initialize the RAG system with FAISS vector store.

        Args:
            persist_directory: Directory to save/load the vector store
        """
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY,
            model="text-embedding-3-small"  # Cost-efficient embeddings
        )
        self.vectorstore: Optional[FAISS] = None
        self.retriever = None

        # Initialize or load vector store
        self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        """Create or load FAISS vector store from fitness knowledge base"""
        try:
            # Create directory if it doesn't exist
            Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
            vectorstore_path = os.path.join(self.persist_directory, "faiss_index")

            # Try to load existing vector store
            if os.path.exists(vectorstore_path):
                print("Loading existing FAISS vector store...")
                self.vectorstore = FAISS.load_local(
                    vectorstore_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True  # Safe in controlled environment
                )
                print(f"Loaded vector store with {self.vectorstore.index.ntotal} documents")
            else:
                print("Creating new FAISS vector store from knowledge base...")
                self._create_vectorstore()

            # Create retriever
            self.retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 3}  # Retrieve top 3 relevant chunks
            )

        except Exception as e:
            print(f"Error initializing vector store: {e}")
            # Fallback: Create new vector store
            self._create_vectorstore()

    def _create_vectorstore(self):
        """Create FAISS vector store from fitness knowledge base"""
        # Split knowledge base into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

        # Create documents from knowledge base
        chunks = text_splitter.split_text(FITNESS_KNOWLEDGE_BASE)
        documents = [
            Document(page_content=chunk, metadata={"source": "fitness_knowledge_base"})
            for chunk in chunks
        ]

        print(f"Creating embeddings for {len(documents)} document chunks...")

        # Create FAISS vector store
        self.vectorstore = FAISS.from_documents(
            documents,
            self.embeddings
        )

        # Save vector store for future use
        vectorstore_path = os.path.join(self.persist_directory, "faiss_index")
        self.vectorstore.save_local(vectorstore_path)
        print(f"Saved vector store to {vectorstore_path}")

    def retrieve(self, query: str, k: int = 3) -> List[Document]:
        """
        Retrieve relevant documents for a query.

        Args:
            query: User query string
            k: Number of documents to retrieve

        Returns:
            List of relevant Document objects
        """
        if not self.vectorstore:
            print("Warning: Vector store not initialized")
            return []

        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []

    def retrieve_context(self, query: str, k: int = 3) -> str:
        """
        Retrieve and format relevant context for a query.

        Args:
            query: User query string
            k: Number of documents to retrieve

        Returns:
            Formatted context string
        """
        documents = self.retrieve(query, k=k)

        if not documents:
            return "No relevant fitness knowledge found."

        # Format context with sources
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"[Source {i}]\n{doc.page_content}\n")

        return "\n".join(context_parts)

    def get_retrieval_qa_chain(self, llm: ChatOpenAI):
        """
        Create a RetrievalQA chain for question answering.

        Args:
            llm: ChatOpenAI instance

        Returns:
            RetrievalQA chain
        """
        if not self.retriever:
            raise ValueError("Retriever not initialized")

        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True
        )


_rag_instance: Optional[FitnessRAG] = None


def get_rag() -> FitnessRAG:
    """
    Get or create the global RAG instance.

    Returns:
        FitnessRAG: Singleton RAG instance
    """
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = FitnessRAG()
    return _rag_instance


def augment_prompt_with_context(query: str, k: int = 3) -> str:
    """
    Augment a user query with relevant fitness context.

    Args:
        query: User's question or request
        k: Number of relevant documents to retrieve

    Returns:
        Augmented prompt with context
    """
    rag = get_rag()
    context = rag.retrieve_context(query, k=k)

    augmented_prompt = f"""Use the following fitness knowledge to help answer the user's question. If the context is relevant, cite it in your response. If the context is not relevant, you can use your general knowledge but mention that.

Context from Fitness Knowledge Base:
{context}

User Question: {query}

Please provide a helpful, accurate response:"""

    return augmented_prompt
