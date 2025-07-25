import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { TimelineStep } from '../types';
import { TimelineViewer } from './TimelineViewer';
import { GanttTimeline } from './GanttTimeline';

interface TimelineViewToggleProps {
  steps: TimelineStep[];
  currentLanguage: string;
  compact?: boolean;
}

type ViewType = 'timeline' | 'checklist' | 'gantt';

export const TimelineViewToggle: React.FC<TimelineViewToggleProps> = ({
  steps,
  currentLanguage,
  compact = false
}) => {
  const { t } = useTranslation();
  const [viewType, setViewType] = useState<ViewType>('timeline');

  const getStepIcon = (status: string): string => {
    switch (status) {
      case 'completed': return '✅';
      case 'in_progress': return '🔄';
      case 'pending': return '⏳';
      default: return '📋';
    }
  };

  const getStepStatus = (status: string): string => {
    switch (status) {
      case 'completed': return currentLanguage === 'zh' ? '已完成' : 'Completed';
      case 'in_progress': return currentLanguage === 'zh' ? '进行中' : 'In Progress';
      case 'pending': return currentLanguage === 'zh' ? '待处理' : 'Pending';
      default: return currentLanguage === 'zh' ? '预估' : 'Estimated';
    }
  };

  const ChecklistView = () => (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">
        ✅ {t('taskChecklist', 'Task Checklist')}
      </h2>
      
      <div className="space-y-3">
        {steps.map((step, index) => (
          <div
            key={step.id}
            className={`flex items-center p-4 rounded-lg border-2 transition-all ${
              step.status === 'completed'
                ? 'border-green-200 bg-green-50'
                : step.status === 'in_progress'
                ? 'border-blue-200 bg-blue-50'
                : 'border-gray-200 bg-gray-50'
            }`}
          >
            <div className="flex-shrink-0 mr-4">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-lg ${
                step.status === 'completed'
                  ? 'bg-green-500 text-white'
                  : step.status === 'in_progress'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-300 text-gray-600'
              }`}>
                {step.status === 'completed' ? '✓' : index + 1}
              </div>
            </div>

            <div className="flex-1">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className={`font-medium ${
                    step.status === 'completed' ? 'text-green-800' : 'text-gray-900'
                  }`}>
                    {currentLanguage === 'zh' ? step.zh.title : step.en.title}
                  </h3>
                  <p className="text-sm text-gray-600 mt-1">
                    {currentLanguage === 'zh' ? step.zh.description : step.en.description}
                  </p>
                </div>
                
                <div className="text-right">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    step.status === 'completed'
                      ? 'bg-green-100 text-green-800'
                      : step.status === 'in_progress'
                      ? 'bg-blue-100 text-blue-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {getStepIcon(step.status)} {getStepStatus(step.status)}
                  </span>
                  
                  {(step.completedDate || step.estimatedDate) && (
                    <div className="text-xs text-gray-500 mt-1">
                      {step.completedDate
                        ? new Date(step.completedDate).toLocaleDateString()
                        : `Est. ${new Date(step.estimatedDate!).toLocaleDateString()}`
                      }
                    </div>
                  )}
                </div>
              </div>

              {/* Progress indicators for task-oriented users */}
              {step.processingTime && (
                <div className="mt-3">
                  <div className="flex items-center text-xs text-gray-600">
                    <span className="mr-2">{t('processingTime', 'Processing Time')}:</span>
                    <div className="flex items-center space-x-4">
                      <span>{t('min', 'Min')}: {step.processingTime.min}d</span>
                      <span>{t('avg', 'Avg')}: {step.processingTime.average}d</span>
                      <span>{t('max', 'Max')}: {step.processingTime.max}d</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Summary Statistics */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h4 className="font-medium text-gray-900 mb-3">
          📊 {t('progressSummary', 'Progress Summary')}
        </h4>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-green-600">
              {steps.filter(s => s.status === 'completed').length}
            </div>
            <div className="text-sm text-gray-600">{t('completed', 'Completed')}</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-blue-600">
              {steps.filter(s => s.status === 'in_progress').length}
            </div>
            <div className="text-sm text-gray-600">{t('inProgress', 'In Progress')}</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-gray-600">
              {steps.filter(s => s.status === 'pending').length}
            </div>
            <div className="text-sm text-gray-600">{t('remaining', 'Remaining')}</div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div>
      {/* View Toggle Controls */}
      <div className="mb-6 flex justify-center">
        <div className="inline-flex rounded-lg border border-gray-200 bg-white p-1">
          <button
            onClick={() => setViewType('timeline')}
            className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
              viewType === 'timeline'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            📅 {t('timelineView', 'Timeline View')}
          </button>
          <button
            onClick={() => setViewType('checklist')}
            className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
              viewType === 'checklist'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            ✅ {t('checklistView', 'Checklist View')}
          </button>
          <button
            onClick={() => setViewType('gantt')}
            className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
              viewType === 'gantt'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            📊 {t('ganttView', 'Chart View')}
          </button>
        </div>
      </div>

      {/* Learning Style Tips */}
      <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
        <div className="flex items-start">
          <span className="text-blue-500 mr-2">💡</span>
          <div className="text-sm text-blue-800">
            {viewType === 'timeline' && (
              <span>
                {currentLanguage === 'zh'
                  ? '时间轴视图：适合喜欢看整体进度和时间关系的用户'
                  : 'Timeline View: Perfect for visual learners who prefer seeing overall progress and time relationships'
                }
              </span>
            )}
            {viewType === 'checklist' && (
              <span>
                {currentLanguage === 'zh'
                  ? '清单视图：适合喜欢逐项完成任务的用户'
                  : 'Checklist View: Ideal for task-oriented users who prefer step-by-step completion'
                }
              </span>
            )}
            {viewType === 'gantt' && (
              <span>
                {currentLanguage === 'zh'
                  ? '图表视图：适合喜欢数据分析和时间规划的用户'
                  : 'Chart View: Great for analytical users who prefer data visualization and time planning'
                }
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Render Selected View */}
      {viewType === 'timeline' && (
        <TimelineViewer
          steps={steps}
          currentLanguage={currentLanguage}
          compact={compact}
        />
      )}
      
      {viewType === 'checklist' && <ChecklistView />}
      
      {viewType === 'gantt' && (
        <GanttTimeline
          steps={steps}
          currentLanguage={currentLanguage}
        />
      )}
    </div>
  );
}; 