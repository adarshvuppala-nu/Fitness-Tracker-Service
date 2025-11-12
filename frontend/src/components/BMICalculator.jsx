import { useState } from 'react';
import { Calculator, TrendingUp, TrendingDown, Minus } from 'lucide-react';

export const BMICalculator = () => {
  const [weight, setWeight] = useState('');
  const [height, setHeight] = useState('');
  const [bmi, setBmi] = useState(null);
  const [category, setCategory] = useState('');

  const calculateBMI = () => {
    if (!weight || !height || weight <= 0 || height <= 0) {
      return;
    }

    const heightInMeters = height / 100;
    const calculatedBMI = (weight / (heightInMeters * heightInMeters)).toFixed(1);
    setBmi(calculatedBMI);

    if (calculatedBMI < 18.5) {
      setCategory('Underweight');
    } else if (calculatedBMI >= 18.5 && calculatedBMI < 25) {
      setCategory('Normal');
    } else if (calculatedBMI >= 25 && calculatedBMI < 30) {
      setCategory('Overweight');
    } else {
      setCategory('Obese');
    }
  };

  const getCategoryColor = () => {
    switch (category) {
      case 'Underweight':
        return 'text-blue-600 dark:text-blue-400';
      case 'Normal':
        return 'text-green-600 dark:text-green-400';
      case 'Overweight':
        return 'text-orange-600 dark:text-orange-400';
      case 'Obese':
        return 'text-red-600 dark:text-red-400';
      default:
        return 'text-gray-600 dark:text-gray-400';
    }
  };

  const getCategoryIcon = () => {
    switch (category) {
      case 'Underweight':
        return <TrendingDown className="w-6 h-6" />;
      case 'Normal':
        return <Minus className="w-6 h-6" />;
      case 'Overweight':
      case 'Obese':
        return <TrendingUp className="w-6 h-6" />;
      default:
        return null;
    }
  };

  const getRecommendation = () => {
    switch (category) {
      case 'Underweight':
        return 'Consider increasing caloric intake with nutrient-dense foods and strength training.';
      case 'Normal':
        return 'Great job! Maintain your healthy weight with balanced diet and regular exercise.';
      case 'Overweight':
        return 'Consider reducing caloric intake and increasing physical activity.';
      case 'Obese':
        return 'Consult with a healthcare provider for a personalized weight management plan.';
      default:
        return '';
    }
  };

  return (
    <div className="group bg-white dark:bg-gray-800 rounded-2xl shadow-elevation-medium hover:shadow-elevation-high transition-all duration-300 p-6 border border-gray-200 dark:border-gray-700">
      <div className="flex items-center gap-3 mb-6">
        <div className="relative">
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-xl blur-md opacity-50" />
          <div className="relative p-3 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-xl shadow-lg">
            <Calculator className="w-5 h-5 text-white" strokeWidth={2} />
          </div>
        </div>
        <h3 className="text-xl font-display font-bold text-gray-900 dark:text-white">
          BMI Calculator
        </h3>
      </div>

      <div className="space-y-5">
        <div>
          <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">
            Weight (kg)
          </label>
          <input
            type="number"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            placeholder="Enter your weight"
            className="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all font-medium"
          />
        </div>

        <div>
          <label className="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">
            Height (cm)
          </label>
          <input
            type="number"
            value={height}
            onChange={(e) => setHeight(e.target.value)}
            placeholder="Enter your height"
            className="w-full px-4 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all font-medium"
          />
        </div>

        <button
          onClick={calculateBMI}
          className="w-full px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white rounded-xl transition-all duration-300 font-bold shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-95"
        >
          Calculate BMI
        </button>

        {bmi && (
          <div className="mt-6 p-6 bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 dark:from-gray-700/80 dark:via-gray-800/80 dark:to-gray-700/80 rounded-2xl border-2 border-indigo-200 dark:border-indigo-800 shadow-lg animate-fade-in-up">
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm font-bold text-gray-600 dark:text-gray-400 uppercase tracking-wide">Your BMI Result</span>
              <div className={`flex items-center gap-2 ${getCategoryColor()}`}>
                {getCategoryIcon()}
                <span className="font-bold text-base">{category}</span>
              </div>
            </div>

            <div className="text-center mb-5">
              <p className="text-6xl font-display font-black bg-gradient-to-br from-indigo-600 to-purple-600 dark:from-indigo-400 dark:to-purple-400 bg-clip-text text-transparent">
                {bmi}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-2 font-medium">Body Mass Index</p>
            </div>

            <div className="relative w-full h-3 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden mb-4 shadow-inner">
              <div className="absolute inset-0 flex">
                <div className="flex-1 bg-gradient-to-r from-blue-400 to-blue-500"></div>
                <div className="flex-1 bg-gradient-to-r from-green-400 to-green-500"></div>
                <div className="flex-1 bg-gradient-to-r from-orange-400 to-orange-500"></div>
                <div className="flex-1 bg-gradient-to-r from-red-400 to-red-500"></div>
              </div>
            </div>

            <div className="text-xs font-bold text-gray-600 dark:text-gray-400 mb-4">
              <div className="flex justify-between px-1">
                <span>&lt;18.5</span>
                <span>18.5-24.9</span>
                <span>25-29.9</span>
                <span>30+</span>
              </div>
            </div>

            <div className="p-4 bg-white/60 dark:bg-gray-900/30 rounded-xl">
              <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed font-medium">
                {getRecommendation()}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
