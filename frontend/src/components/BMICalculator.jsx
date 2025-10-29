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
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
      <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center">
        <div className="p-2 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-lg mr-3">
          <Calculator className="w-5 h-5 text-white" />
        </div>
        BMI Calculator
      </h3>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Weight (kg)
          </label>
          <input
            type="number"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            placeholder="Enter weight"
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Height (cm)
          </label>
          <input
            type="number"
            value={height}
            onChange={(e) => setHeight(e.target.value)}
            placeholder="Enter height"
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>

        <button
          onClick={calculateBMI}
          className="w-full px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors font-medium"
        >
          Calculate BMI
        </button>

        {bmi && (
          <div className="mt-4 p-4 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-800 rounded-xl border border-gray-200 dark:border-gray-600">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm text-gray-600 dark:text-gray-400">Your BMI</span>
              <div className={`flex items-center gap-2 ${getCategoryColor()}`}>
                {getCategoryIcon()}
                <span className="font-bold">{category}</span>
              </div>
            </div>

            <div className="text-center mb-3">
              <p className="text-5xl font-bold text-gray-900 dark:text-white">{bmi}</p>
            </div>

            <div className="relative w-full h-2 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden mb-3">
              <div className="absolute inset-0 flex">
                <div className="flex-1 bg-blue-500"></div>
                <div className="flex-1 bg-green-500"></div>
                <div className="flex-1 bg-orange-500"></div>
                <div className="flex-1 bg-red-500"></div>
              </div>
            </div>

            <div className="text-xs text-gray-500 dark:text-gray-400 mb-3">
              <div className="flex justify-between">
                <span>&lt;18.5</span>
                <span>18.5-24.9</span>
                <span>25-29.9</span>
                <span>30+</span>
              </div>
            </div>

            <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
              {getRecommendation()}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
