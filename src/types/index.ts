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

// Dashboard Types
export interface CaseInfo {
  category: string;
  priorityDate: string;
  uscisCenter: string;
  currentStep: string;
  estimatedCompletion: string;
  caseNumber?: string;
  receipts?: string[];
}

export type TimelineStepStatus = 'completed' | 'in_progress' | 'pending' | 'estimated';

export interface TimelineStep {
  id: string;
  en: {
    title: string;
    description?: string;
    tooltip?: string;
  };
  zh: {
    title: string;
    description?: string;
    tooltip?: string;
  };
  status: TimelineStepStatus;
  completedDate?: string;
  estimatedDate?: string;
  processingTime?: {
    min: number;
    max: number;
    average: number;
  };
}

export type AlertType = 'info' | 'warning' | 'update' | 'reminder';

export interface Alert {
  id: string;
  type: AlertType;
  en: {
    title: string;
    message: string;
  };
  zh: {
    title: string;
    message: string;
  };
  timestamp: string;
  isRead?: boolean;
  actionRequired?: boolean;
}

export interface DocumentResource {
  id: string;
  en: {
    title: string;
    description: string;
    url?: string;
  };
  zh: {
    title: string;
    description: string;
    url?: string;
  };
  category: 'checklist' | 'form' | 'guide' | 'faq';
  relevantSteps?: string[];
}

export interface FAQ {
  id: string;
  en: {
    question: string;
    answer: string;
  };
  zh: {
    question: string;
    answer: string;
  };
  category: string;
  relevantSteps?: string[];
} 