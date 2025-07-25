import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { TimelineStep } from '../types';

interface TimelineViewerProps {
  steps: TimelineStep[];
  currentLanguage: string;
  compact?: boolean;
}

export const TimelineViewer: React.FC<TimelineViewerProps> = ({
  steps,
  currentLanguage,
  compact = false
}) => {
  const { t } = useTranslation();
  const [expandedStep, setExpandedStep] = useState<string | null>(null);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return '✅';
      case 'in_progress': return '🔄';
      case 'pending': return '⏳';
      case 'estimated': return '📋';
      default: return '⚪';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600 bg-green-50 border-green-200';
      case 'in_progress': return 'text-blue-600 bg-blue-50 border-blue-200';
      case 'pending': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'estimated': return 'text-gray-600 bg-gray-50 border-gray-200';
      default: return 'text-gray-400 bg-gray-50 border-gray-200';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString(
      currentLanguage === 'zh' ? 'zh-CN' : 'en-US',
      { year: 'numeric', month: 'short', day: 'numeric' }
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900">
          {compact ? t('recentTimeline', 'Recent Timeline') : t('fullTimeline', 'Full Timeline')}
        </h2>
        {!compact && (
          <div className="text-sm text-gray-500">
            {steps.filter(s => s.status === 'completed').length} / {steps.length} {t('completed', 'completed')}
          </div>
        )}
      </div>

      <div className="relative">
        {/* Timeline Line */}
        <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gray-200"></div>

        {/* Timeline Steps */}
        <div className="space-y-6">
          {(compact ? steps.slice(0, 4) : steps).map((step, index) => (
            <div key={step.id} className="relative flex items-start">
              {/* Timeline Dot */}
              <div className={`relative z-10 flex items-center justify-center w-12 h-12 rounded-full border-2 ${getStatusColor(step.status)}`}>
                <span className="text-lg">{getStatusIcon(step.status)}</span>
              </div>

              {/* Step Content */}
              <div className="flex-1 ml-6">
                <div 
                  className={`cursor-pointer ${compact ? '' : 'hover:bg-gray-50 p-4 rounded-lg'}`}
                  onClick={() => !compact && setExpandedStep(expandedStep === step.id ? null : step.id)}
                >
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-medium text-gray-900">
                      {currentLanguage === 'zh' ? step.zh.title : step.en.title}
                    </h3>
                    <div className="flex items-center space-x-2">
                      {(step.completedDate || step.estimatedDate) && (
                        <span className="text-sm text-gray-500">
                          {step.completedDate ? formatDate(step.completedDate) : formatDate(step.estimatedDate!)}
                        </span>
                      )}
                      {!compact && (
                        <svg
                          className={`w-4 h-4 text-gray-400 transition-transform ${
                            expandedStep === step.id ? 'rotate-180' : ''
                          }`}
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                        </svg>
                      )}
                    </div>
                  </div>

                  {/* Step Description */}
                  {(step.en.description || step.zh.description) && (
                    <p className="text-sm text-gray-600 mt-2">
                      {currentLanguage === 'zh' ? step.zh.description : step.en.description}
                    </p>
                  )}

                  {/* Processing Time Info */}
                  {step.processingTime && (
                    <div className="mt-2 text-xs text-gray-500">
                      {t('processingTime', 'Processing Time')}: {step.processingTime.min}-{step.processingTime.max} {t('months', 'months')} 
                      ({t('average', 'avg')}: {step.processingTime.average} {t('months', 'months')})
                    </div>
                  )}
                </div>

                {/* Expanded Content */}
                {!compact && expandedStep === step.id && (
                  <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                    {(step.en.tooltip || step.zh.tooltip) && (
                      <div className="mb-3">
                        <h4 className="font-medium text-gray-900 mb-2">
                          {t('additionalInfo', 'Additional Information')}
                        </h4>
                        <p className="text-sm text-gray-600">
                          {currentLanguage === 'zh' ? step.zh.tooltip : step.en.tooltip}
                        </p>
                      </div>
                    )}

                    {step.processingTime && (
                      <div className="grid grid-cols-3 gap-4 text-sm">
                        <div className="text-center p-2 bg-white rounded">
                          <div className="font-medium text-gray-900">{step.processingTime.min}</div>
                          <div className="text-gray-500">{t('minMonths', 'Min Months')}</div>
                        </div>
                        <div className="text-center p-2 bg-white rounded">
                          <div className="font-medium text-gray-900">{step.processingTime.average}</div>
                          <div className="text-gray-500">{t('avgMonths', 'Avg Months')}</div>
                        </div>
                        <div className="text-center p-2 bg-white rounded">
                          <div className="font-medium text-gray-900">{step.processingTime.max}</div>
                          <div className="text-gray-500">{t('maxMonths', 'Max Months')}</div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {compact && steps.length > 4 && (
          <div className="mt-6 text-center">
            <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
              {t('viewFullTimeline', 'View Full Timeline')} →
            </button>
          </div>
        )}
      </div>
    </div>
  );
}; 