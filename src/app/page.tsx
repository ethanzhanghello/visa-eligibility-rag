'use client';

import React, { useState } from 'react';
import { QuestionCard } from '../components/QuestionCard';
import { ProgressIndicator } from '../components/ProgressIndicator';
import { ResultCard } from '../components/ResultCard';
import { LanguageToggle } from '../components/LanguageToggle';
import { questions } from '../content/questions';
import { categories } from '../content/categories';
import { determineEligibility } from '../lib/eligibility';
import '../i18n/config';

export default function Home() {
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, boolean>>({});
  const [showResults, setShowResults] = useState(false);

  const handleAnswer = (answer: boolean) => {
    const currentQuestion = questions[currentQuestionIndex];
    setAnswers(prev => ({
      ...prev,
      [currentQuestion.id]: answer
    }));

    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    } else {
      setShowResults(true);
    }
  };

  const handleRestart = () => {
    setCurrentQuestionIndex(0);
    setAnswers({});
    setShowResults(false);
  };

  const handleLanguageChange = (lang: string) => {
    setCurrentLanguage(lang);
  };

  if (showResults) {
    const category = categories.find(
      cat => cat.id === determineEligibility(answers)
    ) || categories[categories.length - 1]; // Default to CONSULT_ATTORNEY

    return (
      <main className="min-h-screen bg-gray-50 py-12 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="mb-8 flex justify-end">
            <LanguageToggle
              currentLanguage={currentLanguage}
              onLanguageChange={handleLanguageChange}
            />
          </div>
          <ResultCard
            category={category}
            currentLanguage={currentLanguage}
            onRestart={handleRestart}
          />
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8 flex justify-end">
          <LanguageToggle
            currentLanguage={currentLanguage}
            onLanguageChange={handleLanguageChange}
          />
        </div>
        <ProgressIndicator
          currentQuestion={currentQuestionIndex + 1}
          totalQuestions={questions.length}
        />
        <QuestionCard
          question={questions[currentQuestionIndex]}
          onAnswer={handleAnswer}
          currentLanguage={currentLanguage}
        />
      </div>
    </main>
  );
} 