import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { DocumentResource, FAQ } from '../types';

interface DocumentsTabProps {
  documents: DocumentResource[];
  faqs: FAQ[];
  currentLanguage: string;
  currentStep: string;
}

export const DocumentsTab: React.FC<DocumentsTabProps> = ({
  documents,
  faqs,
  currentLanguage,
  currentStep
}) => {
  const { t } = useTranslation();
  const [activeSection, setActiveSection] = useState<'overview' | 'documents' | 'faqs'>('overview');
  const [expandedFaq, setExpandedFaq] = useState<string | null>(null);

  const getDocumentIcon = (category: string) => {
    switch (category) {
      case 'checklist': return '✅';
      case 'form': return '📋';
      case 'guide': return '📖';
      case 'faq': return '❓';
      default: return '📄';
    }
  };

  const relevantDocuments = documents.filter(doc => 
    !doc.relevantSteps || doc.relevantSteps.includes(currentStep)
  );

  const relevantFaqs = faqs.filter(faq => 
    !faq.relevantSteps || faq.relevantSteps.includes(currentStep)
  );

  return (
    <div className="space-y-6">
      {/* Section Navigation */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex space-x-4">
          <button
            onClick={() => setActiveSection('overview')}
            className={`px-4 py-2 text-sm font-medium rounded-md ${
              activeSection === 'overview'
                ? 'bg-blue-100 text-blue-800'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            📊 {t('overview', 'Overview')}
          </button>
          <button
            onClick={() => setActiveSection('documents')}
            className={`px-4 py-2 text-sm font-medium rounded-md ${
              activeSection === 'documents'
                ? 'bg-blue-100 text-blue-800'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            📄 {t('documents', 'Documents')} ({relevantDocuments.length})
          </button>
          <button
            onClick={() => setActiveSection('faqs')}
            className={`px-4 py-2 text-sm font-medium rounded-md ${
              activeSection === 'faqs'
                ? 'bg-blue-100 text-blue-800'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            ❓ {t('faqs', 'FAQs')} ({relevantFaqs.length})
          </button>
        </div>
      </div>

      {/* Overview Section */}
      {activeSection === 'overview' && (
        <div className="space-y-6">
          {/* What to Expect Next */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              🔮 {t('whatToExpectNext', 'What to Expect Next')}
            </h3>
            <div className="space-y-4">
              <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h4 className="font-medium text-blue-900 mb-2">
                  {t('currentStepDetails', 'Current Step: Background Checks')}
                </h4>
                <p className="text-sm text-blue-700">
                  {currentLanguage === 'zh' 
                    ? '在生物识别采集后，USCIS通常需要2-3个月来处理您的背景调查。在此期间，您的案件可能会显示为"案件正在审理中"。'
                    : 'After biometrics, USCIS typically takes 2–3 months to process your background checks. During this time, your case may show as "Case Being Reviewed".'
                  }
                </p>
              </div>
              
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <h4 className="font-medium text-green-900 mb-2">
                  {t('nextStep', 'Next Step: Interview Preparation')}
                </h4>
                <p className="text-sm text-green-700">
                  {currentLanguage === 'zh' 
                    ? '一旦背景调查完成，您将收到面试通知。请提前开始准备所需文件和练习可能的面试问题。'
                    : 'Once background checks are complete, you will receive an interview notice. Start preparing required documents and practicing potential interview questions.'
                  }
                </p>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              ⚡ {t('quickActions', 'Quick Actions')}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50">
                <div className="flex items-center">
                  <span className="text-2xl mr-3">📋</span>
                  <div>
                    <h4 className="font-medium text-gray-900">
                      {t('downloadChecklist', 'Download Interview Checklist')}
                    </h4>
                    <p className="text-sm text-gray-600">
                      {t('downloadChecklistDesc', 'Get the complete document list for your interview')}
                    </p>
                  </div>
                </div>
              </button>
              
              <button className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50">
                <div className="flex items-center">
                  <span className="text-2xl mr-3">🏥</span>
                  <div>
                    <h4 className="font-medium text-gray-900">
                      {t('findCivilSurgeon', 'Find Civil Surgeon')}
                    </h4>
                    <p className="text-sm text-gray-600">
                      {t('findCivilSurgeonDesc', 'Locate authorized medical examiners in your area')}
                    </p>
                  </div>
                </div>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Documents Section */}
      {activeSection === 'documents' && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            📄 {t('documentsAndResources', 'Documents & Resources')}
          </h3>
          <div className="space-y-4">
            {relevantDocuments.map((doc) => (
              <div key={doc.id} className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
                <div className="flex items-start justify-between">
                  <div className="flex items-start">
                    <span className="text-xl mr-3">{getDocumentIcon(doc.category)}</span>
                    <div>
                      <h4 className="font-medium text-gray-900">
                        {currentLanguage === 'zh' ? doc.zh.title : doc.en.title}
                      </h4>
                      <p className="text-sm text-gray-600 mt-1">
                        {currentLanguage === 'zh' ? doc.zh.description : doc.en.description}
                      </p>
                      <span className="inline-block mt-2 px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                        {doc.category.charAt(0).toUpperCase() + doc.category.slice(1)}
                      </span>
                    </div>
                  </div>
                  {doc.en.url && (
                    <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                      {t('download', 'Download')} ↓
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Language Specific Downloads */}
          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <h4 className="font-medium text-gray-900 mb-3">
              🌐 {t('languageSpecific', 'Language-Specific Resources')}
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <button className="p-3 bg-white border border-gray-200 rounded text-left hover:bg-gray-50">
                <div className="flex items-center">
                  <span className="mr-2">🇺🇸</span>
                  <span className="font-medium">English Checklist</span>
                </div>
              </button>
              <button className="p-3 bg-white border border-gray-200 rounded text-left hover:bg-gray-50">
                <div className="flex items-center">
                  <span className="mr-2">🇨🇳</span>
                  <span className="font-medium">中文清单</span>
                </div>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* FAQs Section */}
      {activeSection === 'faqs' && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            ❓ {t('frequentlyAskedQuestions', 'Frequently Asked Questions')}
          </h3>
          <div className="space-y-3">
            {relevantFaqs.map((faq) => (
              <div key={faq.id} className="border border-gray-200 rounded-lg">
                <button
                  onClick={() => setExpandedFaq(expandedFaq === faq.id ? null : faq.id)}
                  className="w-full p-4 text-left hover:bg-gray-50 flex items-center justify-between"
                >
                  <span className="font-medium text-gray-900">
                    {currentLanguage === 'zh' ? faq.zh.question : faq.en.question}
                  </span>
                  <svg
                    className={`w-5 h-5 text-gray-500 transition-transform ${
                      expandedFaq === faq.id ? 'rotate-180' : ''
                    }`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                {expandedFaq === faq.id && (
                  <div className="px-4 pb-4">
                    <p className="text-sm text-gray-600">
                      {currentLanguage === 'zh' ? faq.zh.answer : faq.en.answer}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Contact Support */}
          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h4 className="font-medium text-blue-900 mb-2">
              💬 {t('stillHaveQuestions', 'Still have questions?')}
            </h4>
            <p className="text-sm text-blue-700 mb-3">
              {currentLanguage === 'zh' 
                ? '如果您找不到问题的答案，我们的AI助手可以帮助您。'
                : 'If you can\'t find the answer to your question, our AI assistant can help.'
              }
            </p>
            <button className="bg-blue-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-blue-700">
              {t('askChatbot', 'Ask Chatbot Assistant')} 🤖
            </button>
          </div>
        </div>
      )}
    </div>
  );
}; 