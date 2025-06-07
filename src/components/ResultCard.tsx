import React from 'react';
import { useTranslation } from 'react-i18next';
import { CategoryInfo } from '../types';

interface ResultCardProps {
  category: CategoryInfo;
  currentLanguage: string;
  onRestart: () => void;
}

export const ResultCard: React.FC<ResultCardProps> = ({
  category,
  currentLanguage,
  onRestart
}) => {
  const { t } = useTranslation();
  const content = currentLanguage === 'en' ? category.en : category.zh;

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold mb-4">{content.title}</h2>
      <p className="text-gray-700 mb-6">{content.description}</p>
      
      <div className="mb-6">
        <h3 className="text-lg font-medium mb-3">
          {currentLanguage === 'en' ? 'Requirements:' : '要求：'}
        </h3>
        <ul className="list-disc list-inside space-y-2">
          {content.requirements.map((requirement, index) => (
            <li key={index} className="text-gray-600">{requirement}</li>
          ))}
        </ul>
      </div>

      <button
        onClick={onRestart}
        className="w-full py-3 px-6 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
      >
        {t('restart')}
      </button>
    </div>
  );
}; 