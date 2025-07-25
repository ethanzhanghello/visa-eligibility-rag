import React, { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

interface ChatMessage {
  id: string;
  type: 'user' | 'bot';
  message: string;
  timestamp: Date;
  confidence?: number;
}

interface ChatbotWidgetProps {
  currentLanguage: string;
  userContext?: {
    caseInfo?: any;
    currentStep?: string;
  };
}

export const ChatbotWidget: React.FC<ChatbotWidgetProps> = ({
  currentLanguage,
  userContext
}) => {
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (messages.length === 0) {
      // Add welcome message
      const welcomeMessage: ChatMessage = {
        id: 'welcome',
        type: 'bot',
        message: currentLanguage === 'zh' 
          ? '您好！我是您的绿卡申请助手。我可以帮您回答关于申请流程、文件要求和时间安排的问题。请问有什么可以帮助您的吗？'
          : 'Hello! I\'m your green card application assistant. I can help answer questions about the application process, document requirements, and timelines. How can I assist you today?',
        timestamp: new Date()
      };
      setMessages([welcomeMessage]);
    }
  }, [currentLanguage]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: ChatMessage = {
      id: `user_${Date.now()}`,
      type: 'user',
      message: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Simulate API call to RAG system
      // In real implementation, this would call your existing RAG API
      const response = await simulateRAGResponse(inputMessage, currentLanguage, userContext);
      
      const botMessage: ChatMessage = {
        id: `bot_${Date.now()}`,
        type: 'bot',
        message: response.answer,
        timestamp: new Date(),
        confidence: response.confidence
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: `error_${Date.now()}`,
        type: 'bot',
        message: currentLanguage === 'zh' 
          ? '抱歉，我现在无法回答您的问题。请稍后再试或联系人工客服。'
          : 'Sorry, I\'m unable to answer your question right now. Please try again later or contact support.',
        timestamp: new Date(),
        confidence: 0
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const getQuickQuestions = () => {
    const questions = currentLanguage === 'zh' ? [
      '我需要准备哪些文件？',
      '面试时会问什么问题？',
      '我的案件进度正常吗？',
      '如何准备体检？'
    ] : [
      'What documents do I need?',
      'What questions are asked in the interview?',
      'Is my case progressing normally?',
      'How do I prepare for the medical exam?'
    ];

    return questions;
  };

  const handleQuickQuestion = (question: string) => {
    setInputMessage(question);
  };

  return (
    <>
      {/* Floating Chat Button */}
      <div className="fixed bottom-6 right-6 z-50">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="bg-blue-600 hover:bg-blue-700 text-white rounded-full p-4 shadow-lg transition-all duration-200 transform hover:scale-105"
        >
          {isOpen ? (
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          ) : (
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          )}
        </button>

        {/* Notification Badge */}
        {!isOpen && (
          <div className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-6 h-6 flex items-center justify-center">
            🤖
          </div>
        )}
      </div>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 w-96 h-96 bg-white rounded-lg shadow-xl border border-gray-200 z-50 flex flex-col">
          {/* Header */}
          <div className="bg-blue-600 text-white p-4 rounded-t-lg flex items-center justify-between">
            <div className="flex items-center">
              <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center mr-3">
                🤖
              </div>
              <div>
                <h3 className="font-medium">
                  {t('chatbotAssistant', 'AI Assistant')}
                </h3>
                <p className="text-xs text-blue-100">
                  {t('onlineNow', 'Online now')}
                </p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-blue-100 hover:text-white"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 p-4 overflow-y-auto bg-gray-50">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`mb-4 ${message.type === 'user' ? 'text-right' : 'text-left'}`}
              >
                <div
                  className={`inline-block max-w-xs lg:max-w-md px-4 py-2 rounded-lg text-sm ${
                    message.type === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-white text-gray-800 border border-gray-200'
                  }`}
                >
                  {message.message}
                  {message.confidence !== undefined && message.confidence < 0.7 && (
                    <div className="mt-1 text-xs text-yellow-600">
                      {currentLanguage === 'zh' 
                        ? '⚠️ 建议咨询专业律师确认'
                        : '⚠️ Consider consulting a professional for confirmation'
                      }
                    </div>
                  )}
                </div>
                <div className="text-xs text-gray-500 mt-1">
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="text-left mb-4">
                <div className="inline-block bg-white text-gray-800 border border-gray-200 px-4 py-2 rounded-lg">
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                    {t('thinking', 'Thinking...')}
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Questions (shown when no recent messages) */}
          {messages.length <= 1 && (
            <div className="p-3 border-t border-gray-200">
              <p className="text-xs text-gray-600 mb-2">
                {t('quickQuestions', 'Quick questions:')}
              </p>
              <div className="space-y-1">
                {getQuickQuestions().map((question, index) => (
                  <button
                    key={index}
                    onClick={() => handleQuickQuestion(question)}
                    className="w-full text-left text-xs text-blue-600 hover:text-blue-800 p-1 hover:bg-blue-50 rounded"
                  >
                    • {question}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input */}
          <div className="p-4 border-t border-gray-200">
            <div className="flex items-center space-x-2">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={currentLanguage === 'zh' ? '输入您的问题...' : 'Type your question...'}
                className="flex-1 resize-none border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={1}
                disabled={isLoading}
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading || !inputMessage.trim()}
                className="bg-blue-600 text-white rounded-lg p-2 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

// Simulate RAG API response
async function simulateRAGResponse(
  question: string, 
  language: string, 
  context?: any
): Promise<{ answer: string; confidence: number }> {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));

  // Mock responses based on common questions
  const responses = language === 'zh' ? {
    '文件': {
      answer: '对于您的EB-2申请，您需要准备以下主要文件：\n\n1. 表格I-485（调整身份申请）\n2. 表格I-693（体检报告）\n3. 护照复印件\n4. 出生证明\n5. 结婚证（如适用）\n6. 警察证明\n7. 财务支持证明\n8. 雇主支持信\n\n建议您提前准备这些文件，因为有些文件（如体检）有时效要求。',
      confidence: 0.95
    },
    '面试': {
      answer: '绿卡面试通常会问以下问题：\n\n1. 您的工作背景和当前职位\n2. 为什么选择在美国工作\n3. 您的教育背景\n4. 家庭情况\n5. 未来的计划\n6. 是否有犯罪记录\n7. 是否曾经违反移民法\n\n请诚实回答所有问题，并带齐所有要求的文件。',
      confidence: 0.88
    },
    '进度': {
      answer: '根据您的案件信息，您目前处于第3阶段（生物识别已完成），这是正常的进度。对于EB-2类别的中国出生申请人，当前的处理时间通常需要：\n\n• 从生物识别到EAD批准：2-4个月\n• 整个流程预计完成时间：2025年9月\n\n您的进度比65%的同类申请人要快，继续保持！',
      confidence: 0.92
    },
    '体检': {
      answer: '体检准备要点：\n\n1. 寻找USCIS指定的民事外科医生\n2. 带齐疫苗记录\n3. 准备体检费用（通常$200-500）\n4. 体检报告I-693必须密封\n5. 体检有效期为2年\n6. 建议在面试前3个月内完成\n\n注意：体检报告必须由您本人在面试时提交给USCIS官员。',
      confidence: 0.90
    }
  } : {
    'document': {
      answer: 'For your EB-2 application, you\'ll need these key documents:\n\n1. Form I-485 (Application to Adjust Status)\n2. Form I-693 (Medical Examination)\n3. Passport copy\n4. Birth certificate\n5. Marriage certificate (if applicable)\n6. Police certificates\n7. Financial support evidence\n8. Employment letter\n\nI recommend preparing these documents early, as some (like medical exams) have time limitations.',
      confidence: 0.95
    },
    'interview': {
      answer: 'Green card interviews typically include questions about:\n\n1. Your work background and current position\n2. Why you chose to work in the US\n3. Your educational background\n4. Family situation\n5. Future plans\n6. Criminal history\n7. Immigration violations\n\nBe honest with all answers and bring all requested documents.',
      confidence: 0.88
    },
    'progress': {
      answer: 'Based on your case information, you\'re currently at Stage 3 (Biometrics Completed), which is normal progress. For EB-2 China-born applicants, current processing times typically require:\n\n• Biometrics to EAD approval: 2-4 months\n• Total estimated completion: September 2025\n\nYou\'re ahead of 65% of similar applicants - keep it up!',
      confidence: 0.92
    },
    'medical': {
      answer: 'Medical exam preparation:\n\n1. Find a USCIS-designated civil surgeon\n2. Bring vaccination records\n3. Prepare exam fees ($200-500 typically)\n4. I-693 report must be sealed\n5. Medical exam valid for 2 years\n6. Complete within 3 months before interview\n\nNote: You must personally submit the sealed medical report to the USCIS officer during your interview.',
      confidence: 0.90
    }
  };

  // Find matching response
  const questionLower = question.toLowerCase();
  for (const [key, response] of Object.entries(responses)) {
    if (questionLower.includes(key)) {
      return response;
    }
  }

  // Default response for unmatched questions
  return {
    answer: language === 'zh' 
      ? '感谢您的问题。这是一个很好的问题，但我需要更多信息来给您准确的答案。建议您：\n\n1. 查看USCIS官方网站获取最新信息\n2. 咨询您的移民律师\n3. 联系USCIS客服热线\n\n如果您有更具体的问题，我很乐意帮助您。'
      : 'Thank you for your question. This is a great question, but I need more information to give you an accurate answer. I recommend:\n\n1. Check the official USCIS website for latest information\n2. Consult with your immigration attorney\n3. Contact USCIS customer service\n\nIf you have more specific questions, I\'d be happy to help.',
    confidence: 0.6
  };
} 