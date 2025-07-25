'use client';

import React, { useState, useEffect } from 'react';
import { Dashboard } from '../components/Dashboard';
import { sampleTrackingCase } from '../data/sampleTrackingData';
import { convertToCaseInfo, convertToTimelineSteps, generateAlertsFromTracking } from '../utils/trackingDataAdapter';
import { sampleDocuments, sampleFAQs } from '../data/sampleData';
import '../i18n/config';

export default function Home() {
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const [showAdminLink, setShowAdminLink] = useState(false);

  const handleLanguageChange = (lang: string) => {
    setCurrentLanguage(lang);
  };

  // Convert tracking data to dashboard format
  const caseInfo = convertToCaseInfo(sampleTrackingCase);
  const timelineSteps = convertToTimelineSteps(sampleTrackingCase);
  const alerts = generateAlertsFromTracking(sampleTrackingCase);

  return (
    <div className="relative">
      {/* Admin Link (for demo purposes) */}
      <div className="fixed top-4 right-4 z-50">
        <button
          onClick={() => setShowAdminLink(!showAdminLink)}
          className="bg-gray-800 text-white px-3 py-2 rounded-full text-sm hover:bg-gray-700 transition-colors"
        >
          🛠️
        </button>
        {showAdminLink && (
          <div className="absolute right-0 mt-2 bg-white border border-gray-200 rounded-lg shadow-lg p-4 min-w-[200px]">
            <h3 className="font-medium text-gray-900 mb-2">Admin Tools</h3>
            <a 
              href="/admin" 
              className="block w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded"
            >
              🏛️ Admin Portal
            </a>
            <div className="border-t border-gray-200 my-2"></div>
            <p className="text-xs text-gray-500">
              Demo: Access admin portal to manage case stages
            </p>
          </div>
        )}
      </div>

      {/* Real-time Case Status Banner */}
      <div className="bg-blue-600 text-white px-4 py-2 text-center text-sm">
        📊 Case {sampleTrackingCase.case_number} • Stage {sampleTrackingCase.current_stage_id} • 
        Next: {sampleTrackingCase.next_step_estimate.stage_name} (Est. {new Date(sampleTrackingCase.next_step_estimate.expected_date).toLocaleDateString()})
      </div>

      <Dashboard
        currentLanguage={currentLanguage}
        onLanguageChange={handleLanguageChange}
        caseInfo={caseInfo}
        timelineSteps={timelineSteps}
        alerts={alerts}
        documents={sampleDocuments}
        faqs={sampleFAQs}
      />
    </div>
  );
} 