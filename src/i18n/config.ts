import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        translation: {
          language: 'Language',
          start: 'Start Screening',
          next: 'Next',
          previous: 'Previous',
          yes: 'Yes',
          no: 'No',
          results: 'Results',
          consultAttorney: 'Consult an Immigration Attorney',
          restart: 'Restart Screening'
        }
      },
      zh: {
        translation: {
          language: '语言',
          start: '开始评估',
          next: '下一步',
          previous: '上一步',
          yes: '是',
          no: '否',
          results: '结果',
          consultAttorney: '咨询移民律师',
          restart: '重新开始评估'
        }
      }
    },
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n; 