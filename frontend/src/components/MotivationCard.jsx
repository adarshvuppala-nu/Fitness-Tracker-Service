import { Sparkles, TrendingUp } from 'lucide-react';
import { useEffect, useState } from 'react';

const motivationalQuotes = [
  { text: "The only bad workout is the one that didn't happen.", author: "AD" },
  { text: "Your body can stand almost anything. It's your mind you have to convince.", author: "AD" },
  { text: "Don't limit your challenges, challenge your limits.", author: "AD" },
  { text: "The pain you feel today will be the strength you feel tomorrow.", author: "AD" },
  { text: "Success starts with self-discipline.", author: "AD" },
  { text: "Push yourself because no one else is going to do it for you.", author: "AD" },
  { text: "Great things never come from comfort zones.", author: "AD" },
  { text: "Dream it. Wish it. Do it.", author: "AD" },
  { text: "Success doesn't just find you. You have to go out and get it.", author: "AD" },
  { text: "The harder you work for something, the greater you'll feel when you achieve it.", author: "AD" },
];

export const MotivationCard = () => {
  const [quote, setQuote] = useState(motivationalQuotes[0]);

  useEffect(() => {
    // Get quote of the day based on date
    const dayOfYear = Math.floor((new Date() - new Date(new Date().getFullYear(), 0, 0)) / 86400000);
    const quoteIndex = dayOfYear % motivationalQuotes.length;
    setQuote(motivationalQuotes[quoteIndex]);
  }, []);

  return (
    <div className="relative group overflow-hidden bg-gradient-primary rounded-2xl shadow-elevation-high hover:shadow-elevation-high transition-all duration-500 p-6 border-2 border-white/20">
      {/* Animated background pattern */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,rgba(255,255,255,0.1),transparent)] animate-pulse-slow" />

      {/* Content */}
      <div className="relative z-10">
        <div className="flex items-center gap-2 mb-4">
          <div className="p-2 bg-white/20 rounded-xl backdrop-blur-sm">
            <Sparkles className="w-5 h-5 text-white animate-pulse" strokeWidth={2.5} />
          </div>
          <span className="text-sm font-bold text-white/90 uppercase tracking-wider">
            Daily Motivation
          </span>
        </div>

        <blockquote className="mb-4">
          <p className="text-lg font-display font-bold text-white leading-relaxed mb-2">
            "{quote.text}"
          </p>
          <footer className="text-sm font-medium text-white/80">
            — {quote.author}
          </footer>
        </blockquote>

        <div className="flex items-center gap-2 text-white/90">
          <TrendingUp className="w-4 h-4" strokeWidth={2.5} />
          <span className="text-xs font-bold">Keep pushing forward!</span>
        </div>
      </div>

      {/* Decorative elements */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full blur-3xl" />
      <div className="absolute bottom-0 left-0 w-24 h-24 bg-white/10 rounded-full blur-2xl" />
    </div>
  );
};
