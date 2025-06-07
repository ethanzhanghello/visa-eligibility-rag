import { GreenCardCategory } from '../types';

interface Answers {
  [key: string]: boolean;
}

export function determineEligibility(answers: Answers): GreenCardCategory {
  // Family-based immediate relative
  if (answers['q3']) {
    return 'FAMILY_BASED_IMMEDIATE';
  }

  // EB-2
  if (answers['q1'] && answers['q2'] && answers['q5']) {
    return 'EB2';
  }

  // If no clear category is determined, recommend consulting an attorney
  return 'CONSULT_ATTORNEY';
}

export function getNextQuestion(currentQuestionId: string, answers: Answers): string | null {
  const questionOrder = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6'];
  const currentIndex = questionOrder.indexOf(currentQuestionId);
  
  // If we're at the last question or can determine eligibility, return null
  if (currentIndex === questionOrder.length - 1) {
    return null;
  }

  // Skip to the next question
  return questionOrder[currentIndex + 1];
} 