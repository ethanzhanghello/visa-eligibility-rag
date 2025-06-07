export type QuestionType = 'boolean' | 'multiple_choice' | 'text';

export interface Question {
  id: string;
  en: string;
  zh: string;
  type: QuestionType;
  options?: {
    en: string;
    zh: string;
    value: string;
  }[];
}

export type GreenCardCategory = 
  | 'FAMILY_BASED_IMMEDIATE'
  | 'FAMILY_BASED_PREFERENCE'
  | 'EB1'
  | 'EB2'
  | 'EB3'
  | 'NOT_ELIGIBLE'
  | 'CONSULT_ATTORNEY';

export interface CategoryInfo {
  id: GreenCardCategory;
  en: {
    title: string;
    description: string;
    requirements: string[];
  };
  zh: {
    title: string;
    description: string;
    requirements: string[];
  };
} 