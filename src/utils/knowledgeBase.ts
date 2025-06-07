import faqs from '../data/knowledge-base/faqs.json';

export interface FAQ {
  id: string;
  language: 'en' | 'zh';
  question: string;
  answer: string;
}

export interface KnowledgeBase {
  faqs: FAQ[];
}

export const knowledgeBase: KnowledgeBase = faqs;

export function getFAQsByLanguage(language: 'en' | 'zh'): FAQ[] {
  return knowledgeBase.faqs.filter(faq => faq.language === language);
}

export function getFAQById(id: string): FAQ | undefined {
  return knowledgeBase.faqs.find(faq => faq.id === id);
}

export function getRelatedFAQs(question: string, language: 'en' | 'zh'): FAQ[] {
  // This is a simple implementation. In a real RAG system, this would use
  // vector similarity search or other semantic matching techniques.
  const relevantFAQs = knowledgeBase.faqs.filter(faq => 
    faq.language === language &&
    (faq.question.toLowerCase().includes(question.toLowerCase()) ||
     faq.answer.toLowerCase().includes(question.toLowerCase()))
  );
  return relevantFAQs;
} 