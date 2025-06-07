import React from 'react';
import { useTranslation } from 'react-i18next';

interface LanguageToggleProps {
  currentLanguage: string;
  onLanguageChange: (lang: string) => void;
}

export const LanguageToggle: React.FC<LanguageToggleProps> = ({
  currentLanguage,
  onLanguageChange
}) => {
  const { t } = useTranslation();

  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-gray-600">{t('language')}:</span>
      <button
        onClick={() => onLanguageChange('en')}
        className={`px-3 py-1 rounded ${
          currentLanguage === 'en'
            ? 'bg-blue-500 text-white'
            : 'bg-gray-200 text-gray-700'
        }`}
      >
        English
      </button>
      <button
        onClick={() => onLanguageChange('zh')}
        className={`px-3 py-1 rounded ${
          currentLanguage === 'zh'
            ? 'bg-blue-500 text-white'
            : 'bg-gray-200 text-gray-700'
        }`}
      >
        中文
      </button>
    </div>
  );
}; 