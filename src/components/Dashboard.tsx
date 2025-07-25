import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { NavigationHeader } from './NavigationHeader';
import { MobileTabNavigation } from './MobileTabNavigation';
import { CaseSummaryCard } from './CaseSummaryCard';
import { TimelineViewer } from './TimelineViewer';
import { AlertsTab } from './AlertsTab';
import { DocumentsTab } from './DocumentsTab';
import { CaseInfo, TimelineStep, Alert, DocumentResource, FAQ } from '../types';

interface DashboardProps {
  currentLanguage: string;
  onLanguageChange: (lang: string) => void;
  caseInfo: CaseInfo;
  timelineSteps: TimelineStep[];
  alerts: Alert[];
  documents: DocumentResource[];
  faqs: FAQ[];
}

type TabType = 'dashboard' | 'timeline' | 'alerts' | 'documents';

export const Dashboard: React.FC<DashboardProps> = ({
  currentLanguage,
  onLanguageChange,
  caseInfo,
  timelineSteps,
  alerts,
  documents,
  faqs
}) => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState<TabType>('dashboard');

  const tabs = [
    { id: 'dashboard', label: t('dashboard', 'Dashboard'), icon: '🏠' },
    { id: 'timeline', label: t('timeline', 'Timeline'), icon: '📅' },
    { id: 'alerts', label: t('alerts', 'Alerts'), icon: '🔔' },
    { id: 'documents', label: t('documents', 'Documents'), icon: '📄' }
  ];

  const unreadAlerts = alerts.filter(alert => !alert.isRead).length;

  return (
    <div className="min-h-screen bg-gray-50">
      <NavigationHeader
        currentLanguage={currentLanguage}
        onLanguageChange={onLanguageChange}
        userSession={{ id: 'USER123', name: 'John Doe' }}
      />

      {/* Tab Navigation */}
      <MobileTabNavigation
        tabs={tabs}
        activeTab={activeTab}
        onTabChange={(tabId) => setActiveTab(tabId as TabType)}
        unreadCount={unreadAlerts}
      />

      {/* Tab Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'dashboard' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <CaseSummaryCard
                caseInfo={caseInfo}
                timelineSteps={timelineSteps}
                currentLanguage={currentLanguage}
              />
            </div>
            <div>
              <TimelineViewer
                steps={timelineSteps}
                currentLanguage={currentLanguage}
                compact={true}
              />
            </div>
          </div>
        )}

        {activeTab === 'timeline' && (
          <TimelineViewer
            steps={timelineSteps}
            currentLanguage={currentLanguage}
            compact={false}
          />
        )}

        {activeTab === 'alerts' && (
          <AlertsTab
            alerts={alerts}
            currentLanguage={currentLanguage}
          />
        )}

        {activeTab === 'documents' && (
          <DocumentsTab
            documents={documents}
            faqs={faqs}
            currentLanguage={currentLanguage}
            currentStep={caseInfo.currentStep}
          />
        )}
      </div>
    </div>
  );
}; 