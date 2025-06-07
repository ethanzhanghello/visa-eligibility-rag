import { CategoryInfo } from '../types';

export const categories: CategoryInfo[] = [
  {
    id: 'FAMILY_BASED_IMMEDIATE',
    en: {
      title: 'Family-Based (Immediate Relative)',
      description: 'You may qualify for a green card as an immediate relative of a U.S. citizen.',
      requirements: [
        'Must be married to a U.S. citizen',
        'Must be a parent of a U.S. citizen (if the U.S. citizen is 21 or older)',
        'Must be an unmarried child under 21 of a U.S. citizen'
      ]
    },
    zh: {
      title: '家庭类（直系亲属）',
      description: '作为美国公民的直系亲属，您可能符合绿卡申请条件。',
      requirements: [
        '必须与美国公民结婚',
        '必须是美国公民的父母（如果美国公民年满21岁）',
        '必须是美国公民的21岁以下未婚子女'
      ]
    }
  },
  {
    id: 'EB2',
    en: {
      title: 'Employment-Based (EB-2)',
      description: 'You may qualify for an EB-2 green card based on your advanced degree and job offer.',
      requirements: [
        'Must have an advanced degree (Master\'s or higher)',
        'Must have a job offer from a U.S. employer',
        'Must have a PERM labor certification (unless applying for National Interest Waiver)'
      ]
    },
    zh: {
      title: '就业类（EB-2）',
      description: '基于您的高等学位和工作机会，您可能符合EB-2绿卡申请条件。',
      requirements: [
        '必须拥有高等学位（硕士或更高）',
        '必须获得美国雇主的工作机会',
        '必须获得PERM劳工认证（除非申请国家利益豁免）'
      ]
    }
  },
  {
    id: 'CONSULT_ATTORNEY',
    en: {
      title: 'Consult an Immigration Attorney',
      description: 'Your case may be more complex. We recommend consulting with an immigration attorney for personalized guidance.',
      requirements: [
        'Your situation may involve multiple factors',
        'You may qualify for multiple categories',
        'Your case may require special consideration'
      ]
    },
    zh: {
      title: '咨询移民律师',
      description: '您的情况可能较为复杂。我们建议您咨询移民律师以获取个性化指导。',
      requirements: [
        '您的情况可能涉及多个因素',
        '您可能符合多个类别的条件',
        '您的案件可能需要特殊考虑'
      ]
    }
  }
]; 