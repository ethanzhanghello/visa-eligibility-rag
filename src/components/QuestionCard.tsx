import React from 'react';
import { useTranslation } from 'react-i18next';
import { Question } from '../types';

interface QuestionCardProps {
  question: Question;
  onAnswer: (answer: boolean) => void;
  currentLanguage: string;
}

export const QuestionCard: React.FC<QuestionCardProps> = ({
  question,
  onAnswer,
  currentLanguage
}) => {
  const { t } = useTranslation();

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold mb-6">
        {currentLanguage === 'en' ? question.en : question.zh}
      </h2>
      <div className="flex gap-4">
        <button
          onClick={() => onAnswer(true)}
          className="flex-1 py-3 px-6 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
        >
          {t('yes')}
        </button>
        <button
          onClick={() => onAnswer(false)}
          className="flex-1 py-3 px-6 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
        >
          {t('no')}
        </button>
      </div>
    </div>
  );
}; 