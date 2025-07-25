import React from 'react';
import { useTranslation } from 'react-i18next';
import { CaseInfo, TimelineStep } from '../types';

interface CaseSummaryCardProps {
  caseInfo: CaseInfo;
  timelineSteps: TimelineStep[];
  currentLanguage: string;
}

export const CaseSummaryCard: React.FC<CaseSummaryCardProps> = ({
  caseInfo,
  timelineSteps,
  currentLanguage
}) => {
  const { t } = useTranslation();

  const completedSteps = timelineSteps.filter(step => step.status === 'completed').length;
  const totalSteps = timelineSteps.length;
  const progressPercentage = (completedSteps / totalSteps) * 100;

  const summaryFields = [
    { 
      label: t('category', 'Category'), 
      value: caseInfo.category,
      icon: '📋'
    },
    { 
      label: t('priorityDate', 'Priority Date'), 
      value: caseInfo.priorityDate,
      icon: '📅'
    },
    { 
      label: t('uscisCenter', 'USCIS Center'), 
      value: caseInfo.uscisCenter,
      icon: '🏢'
    },
    { 
      label: t('currentStep', 'Current Step'), 
      value: caseInfo.currentStep,
      icon: '⚡'
    },
    { 
      label: t('estimatedCompletion', 'Estimated Completion'), 
      value: caseInfo.estimatedCompletion,
      icon: '🎯'
    }
  ];

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900">
          {t('caseSummary', 'Case Summary')}
        </h2>
        <div className="flex items-center text-sm text-gray-500">
          <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
          {t('active', 'Active')}
        </div>
      </div>

      {/* Case Details */}
      <div className="space-y-4 mb-6">
        {summaryFields.map((field, index) => (
          <div key={index} className="flex items-center justify-between">
            <div className="flex items-center">
              <span className="mr-3 text-lg">{field.icon}</span>
              <span className="text-sm font-medium text-gray-600">
                {field.label}
              </span>
            </div>
            <span className="text-sm text-gray-900 font-medium">
              {field.value}
            </span>
          </div>
        ))}
      </div>

      {/* Progress Section */}
      <div className="border-t border-gray-200 pt-6">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-medium text-gray-900">
            {t('overallProgress', 'Overall Progress')}
          </h3>
          <span className="text-sm text-gray-600">
            {completedSteps}/{totalSteps} {t('steps', 'steps')}
          </span>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
          <div
            className="bg-gradient-to-r from-blue-500 to-green-500 h-3 rounded-full transition-all duration-500"
            style={{ width: `${progressPercentage}%` }}
          />
        </div>

        {/* Progress Steps */}
        <div className="flex justify-between">
          {timelineSteps.slice(0, 6).map((step, index) => (
            <div key={step.id} className="flex flex-col items-center">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium ${
                step.status === 'completed' 
                  ? 'bg-green-500 text-white' 
                  : step.status === 'in_progress'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-600'
              }`}>
                {step.status === 'completed' ? '✓' : index + 1}
              </div>
              <span className="text-xs text-gray-600 mt-2 text-center max-w-[60px]">
                {currentLanguage === 'zh' ? step.zh.title : step.en.title}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Case Number */}
      {caseInfo.caseNumber && (
        <div className="border-t border-gray-200 pt-4 mt-4">
          <div className="text-xs text-gray-500">
            {t('caseNumber', 'Case Number')}: {caseInfo.caseNumber}
          </div>
        </div>
      )}
    </div>
  );
}; 