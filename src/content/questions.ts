import { Question } from '../types';

export const questions: Question[] = [
  {
    id: 'q1',
    en: 'Are you currently employed in the U.S. with a visa?',
    zh: '你现在是否持有签证在美国工作？',
    type: 'boolean'
  },
  {
    id: 'q2',
    en: 'Do you have a Master\'s degree or higher?',
    zh: '您是否拥有硕士或更高学位？',
    type: 'boolean'
  },
  {
    id: 'q3',
    en: 'Are you married to a U.S. citizen or green card holder?',
    zh: '您是否与美国公民或绿卡持有者结婚？',
    type: 'boolean'
  },
  {
    id: 'q4',
    en: 'Are you related to a U.S. citizen or permanent resident?',
    zh: '您是否与美国公民或永久居民有亲属关系？',
    type: 'boolean'
  },
  {
    id: 'q5',
    en: 'Has a U.S. employer offered you a full-time job?',
    zh: '是否有美国雇主为您提供全职工作？',
    type: 'boolean'
  },
  {
    id: 'q6',
    en: 'Do you plan to self-petition based on extraordinary ability or national interest?',
    zh: '您是否计划基于特殊才能或国家利益进行自我申请？',
    type: 'boolean'
  }
]; 