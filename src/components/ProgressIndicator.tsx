import React from 'react';
import { useTranslation } from 'react-i18next';

interface ProgressIndicatorProps {
  currentQuestion: number;
  totalQuestions: number;
}

export const ProgressIndicator: React.FC<ProgressIndicatorProps> = ({
  currentQuestion,
  totalQuestions
}) => {
  const { t } = useTranslation();
  const progress = (currentQuestion / totalQuestions) * 100;

  return (
    <div className="w-full max-w-2xl mx-auto mb-8">
      <div className="flex justify-between mb-2">
        <span className="text-sm text-gray-600">
          {t('question')} {currentQuestion} / {totalQuestions}
        </span>
        <span className="text-sm text-gray-600">{Math.round(progress)}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2.5">
        <div
          className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  );
}; 