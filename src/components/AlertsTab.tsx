import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Alert } from '../types';

interface AlertsTabProps {
  alerts: Alert[];
  currentLanguage: string;
}

export const AlertsTab: React.FC<AlertsTabProps> = ({
  alerts,
  currentLanguage
}) => {
  const { t } = useTranslation();
  const [filter, setFilter] = useState<'all' | 'unread' | 'important'>('all');

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'info': return '📌';
      case 'warning': return '⚠️';
      case 'update': return '🔄';
      case 'reminder': return '📝';
      default: return '📌';
    }
  };

  const getAlertColor = (type: string) => {
    switch (type) {
      case 'info': return 'bg-blue-50 border-blue-200 text-blue-800';
      case 'warning': return 'bg-yellow-50 border-yellow-200 text-yellow-800';
      case 'update': return 'bg-green-50 border-green-200 text-green-800';
      case 'reminder': return 'bg-purple-50 border-purple-200 text-purple-800';
      default: return 'bg-gray-50 border-gray-200 text-gray-800';
    }
  };

  const filteredAlerts = alerts.filter(alert => {
    if (filter === 'unread') return !alert.isRead;
    if (filter === 'important') return alert.actionRequired;
    return true;
  });

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);

    if (diffInHours < 24) {
      return t('today', 'Today');
    } else if (diffInHours < 48) {
      return t('yesterday', 'Yesterday');
    } else {
      return date.toLocaleDateString(
        currentLanguage === 'zh' ? 'zh-CN' : 'en-US',
        { month: 'short', day: 'numeric' }
      );
    }
  };

  return (
    <div className="space-y-6">
      {/* Filter Controls */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">
            {t('notifications', 'Notifications')}
          </h2>
          <div className="flex space-x-2">
            <button
              onClick={() => setFilter('all')}
              className={`px-3 py-1 text-sm rounded-md ${
                filter === 'all' 
                  ? 'bg-blue-100 text-blue-800' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {t('all', 'All')} ({alerts.length})
            </button>
            <button
              onClick={() => setFilter('unread')}
              className={`px-3 py-1 text-sm rounded-md ${
                filter === 'unread' 
                  ? 'bg-blue-100 text-blue-800' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {t('unread', 'Unread')} ({alerts.filter(a => !a.isRead).length})
            </button>
            <button
              onClick={() => setFilter('important')}
              className={`px-3 py-1 text-sm rounded-md ${
                filter === 'important' 
                  ? 'bg-blue-100 text-blue-800' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {t('important', 'Important')} ({alerts.filter(a => a.actionRequired).length})
            </button>
          </div>
        </div>
      </div>

      {/* Timeline Alerts Section */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          📅 {t('upcomingTimelineAlerts', 'Upcoming Timeline Alerts')}
        </h3>
        <div className="space-y-3">
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                  <span className="text-white text-sm font-medium">!</span>
                </div>
              </div>
              <div className="ml-3">
                <h4 className="font-medium text-blue-900">
                  {t('interviewNoticeExpected', 'Interview Notice Expected')}
                </h4>
                <p className="text-sm text-blue-700 mt-1">
                  {currentLanguage === 'zh' 
                    ? '您预计将在接下来的3-6周内收到面试通知。'
                    : 'You are expected to receive an interview notice in the next 3–6 weeks.'
                  }
                </p>
              </div>
            </div>
          </div>

          <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-yellow-500 rounded-full flex items-center justify-center">
                  <span className="text-white text-sm font-medium">📋</span>
                </div>
              </div>
              <div className="ml-3">
                <h4 className="font-medium text-yellow-900">
                  {t('medicalExamReminder', 'Medical Exam Reminder')}
                </h4>
                <p className="text-sm text-yellow-700 mt-1">
                  {currentLanguage === 'zh' 
                    ? '请在面试前完成Form I-693（体检表）。'
                    : 'Form I-693 (Medical Exam) should be completed before your interview.'
                  }
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Notifications */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          🔔 {t('recentNotifications', 'Recent Notifications')}
        </h3>
        <div className="space-y-4">
          {filteredAlerts.length > 0 ? (
            filteredAlerts.map((alert) => (
              <div
                key={alert.id}
                className={`p-4 border rounded-lg ${getAlertColor(alert.type)} ${
                  !alert.isRead ? 'ring-2 ring-blue-200' : ''
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start">
                    <span className="text-lg mr-3">{getAlertIcon(alert.type)}</span>
                    <div>
                      <h4 className="font-medium">
                        {currentLanguage === 'zh' ? alert.zh.title : alert.en.title}
                      </h4>
                      <p className="text-sm mt-1">
                        {currentLanguage === 'zh' ? alert.zh.message : alert.en.message}
                      </p>
                      {alert.actionRequired && (
                        <span className="inline-block mt-2 px-2 py-1 bg-red-100 text-red-800 text-xs rounded">
                          {t('actionRequired', 'Action Required')}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="text-xs text-gray-500 flex flex-col items-end">
                    <span>{formatTimestamp(alert.timestamp)}</span>
                    {!alert.isRead && (
                      <span className="w-2 h-2 bg-blue-500 rounded-full mt-1"></span>
                    )}
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-8 text-gray-500">
              <span className="text-4xl mb-2 block">📭</span>
              {t('noAlerts', 'No alerts match your current filter')}
            </div>
          )}
        </div>
      </div>

      {/* Policy Watch Section */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          🏛️ {t('policyWatch', 'Policy Watch')}
        </h3>
        <div className="space-y-4">
          <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
            <div className="flex items-start">
              <span className="text-lg mr-3">📄</span>
              <div>
                <h4 className="font-medium text-gray-900">
                  {currentLanguage === 'zh' 
                    ? '法案提议改变EB-2积压情况'
                    : 'Bill proposes changes to EB-2 backlog'
                  }
                </h4>
                <p className="text-sm text-gray-600 mt-1">
                  {currentLanguage === 'zh' 
                    ? '国会正在考虑一项新法案，可能会影响EB-2类别的处理时间。'
                    : 'Congress is considering new legislation that may impact EB-2 category processing times.'
                  }
                </p>
                <span className="text-xs text-gray-500 mt-2 block">2 days ago</span>
              </div>
            </div>
          </div>

          <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
            <div className="flex items-start">
              <span className="text-lg mr-3">🏢</span>
              <div>
                <h4 className="font-medium text-gray-900">
                  {currentLanguage === 'zh' 
                    ? '国务院为中国出生申请人增加领事处理预约'
                    : 'State Department adds consular processing appointments for China-born applicants'
                  }
                </h4>
                <p className="text-sm text-gray-600 mt-1">
                  {currentLanguage === 'zh' 
                    ? '广州总领事馆增加了更多面试时段。'
                    : 'Additional interview slots have been added at the Guangzhou consulate.'
                  }
                </p>
                <span className="text-xs text-gray-500 mt-2 block">1 week ago</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}; 