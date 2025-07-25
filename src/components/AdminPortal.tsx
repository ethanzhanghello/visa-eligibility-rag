import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { UserCaseTracker, CaseUpdate, StageUpdateRequest } from '../types/tracking';
import { DEFAULT_STAGES } from '../data/trackingConfig';

interface AdminPortalProps {
  currentLanguage: string;
}

export const AdminPortal: React.FC<AdminPortalProps> = ({ currentLanguage }) => {
  const { t } = useTranslation();
  const [cases, setCases] = useState<UserCaseTracker[]>([]);
  const [selectedCase, setSelectedCase] = useState<UserCaseTracker | null>(null);
  const [recentUpdates, setRecentUpdates] = useState<CaseUpdate[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    initializeData();
  }, []);

  const initializeData = async () => {
    // Check if data is populated, if not, populate it
    try {
      const statusResponse = await fetch('/api/tracking/populate');
      const statusResult = await statusResponse.json();
      
      if (!statusResult.data.populated) {
        // Populate sample data
        await fetch('/api/tracking/populate', { method: 'POST' });
      }
    } catch (error) {
      console.error('Failed to initialize data:', error);
    }
    
    // Fetch the data
    await fetchCases();
    await fetchRecentUpdates();
  };

  const fetchCases = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/tracking/cases');
      const result = await response.json();
      if (result.success) {
        setCases(result.data.cases);
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Failed to fetch cases');
    } finally {
      setLoading(false);
    }
  };

  const fetchRecentUpdates = async () => {
    try {
      const response = await fetch('/api/tracking/stages/updates?limit=20');
      const result = await response.json();
      if (result.success) {
        setRecentUpdates(result.data);
      }
    } catch (err) {
      console.error('Failed to fetch updates:', err);
    }
  };

  const markStageComplete = async (caseId: string, stageId: number, notes?: string) => {
    setLoading(true);
    try {
      const updateRequest: StageUpdateRequest = {
        case_id: caseId,
        stage_id: stageId,
        completed: true,
        date_completed: new Date().toISOString().split('T')[0],
        notes: notes
      };

      const response = await fetch('/api/tracking/stages/complete', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateRequest)
      });

      const result = await response.json();
      if (result.success) {
        // Update local state
        setCases(prevCases => 
          prevCases.map(c => c.user_id === caseId ? result.data : c)
        );
        setSelectedCase(result.data);
        await fetchRecentUpdates();
        setError(null);
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Failed to update stage');
    } finally {
      setLoading(false);
    }
  };

  const getStageStatus = (stage: any) => {
    if (stage.completed) {
      return { icon: '✅', color: 'text-green-600', bg: 'bg-green-50' };
    } else if (stage.stage_id === selectedCase?.current_stage_id) {
      return { icon: '🔄', color: 'text-blue-600', bg: 'bg-blue-50' };
    } else {
      return { icon: '⏳', color: 'text-gray-600', bg: 'bg-gray-50' };
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getCasesByStage = () => {
    const stageGroups: { [stageId: number]: UserCaseTracker[] } = {};
    
    cases.forEach(caseItem => {
      const currentStage = caseItem.current_stage_id;
      if (!stageGroups[currentStage]) {
        stageGroups[currentStage] = [];
      }
      stageGroups[currentStage].push(caseItem);
    });

    return stageGroups;
  };

  if (loading && cases.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading admin portal...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-2xl font-bold text-gray-900">
            🛠️ Admin Portal - Case Tracking System
          </h1>
          <p className="text-gray-600 mt-1">
            Manage and update green card application stages
          </p>
        </div>
      </div>

      {error && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="bg-red-50 border border-red-200 rounded-md p-4">
            <p className="text-red-800">{error}</p>
          </div>
        </div>
      )}

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Cases Overview */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                📊 Cases Overview
              </h2>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Total Cases</span>
                  <span className="font-semibold text-gray-900">{cases.length}</span>
                </div>
                {Object.entries(getCasesByStage()).map(([stageId, casesInStage]) => {
                  const stage = DEFAULT_STAGES.find(s => s.stage_id === parseInt(stageId));
                  return (
                    <div key={stageId} className="flex justify-between items-center">
                      <span className="text-gray-600 text-sm">{stage?.name}</span>
                      <span className="text-sm font-medium">{casesInStage.length}</span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Cases List */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                📋 All Cases
              </h3>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {cases.map((caseItem) => (
                  <div
                    key={caseItem.user_id}
                    onClick={() => setSelectedCase(caseItem)}
                    className={`p-3 border rounded-lg cursor-pointer hover:bg-gray-50 ${
                      selectedCase?.user_id === caseItem.user_id ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
                    }`}
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-medium text-gray-900">{caseItem.case_number}</p>
                        <p className="text-sm text-gray-600">{caseItem.visa_type}</p>
                        <p className="text-xs text-gray-500">{caseItem.processing_center}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-xs text-gray-500">Stage {caseItem.current_stage_id}</p>
                        <p className="text-xs text-gray-500">{formatDate(caseItem.updated_at)}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Case Details */}
          <div className="lg:col-span-2">
            {selectedCase ? (
              <div className="space-y-6">
                {/* Case Info */}
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h2 className="text-lg font-semibold text-gray-900 mb-4">
                    📁 Case Details: {selectedCase.case_number}
                  </h2>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-600">Visa Type:</span>
                      <span className="ml-2 font-medium">{selectedCase.visa_type}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Processing Center:</span>
                      <span className="ml-2 font-medium">{selectedCase.processing_center}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Priority Date:</span>
                      <span className="ml-2 font-medium">{formatDate(selectedCase.priority_date)}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Country of Birth:</span>
                      <span className="ml-2 font-medium">{selectedCase.country_of_birth}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Current Stage:</span>
                      <span className="ml-2 font-medium">Stage {selectedCase.current_stage_id}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Est. Completion:</span>
                      <span className="ml-2 font-medium">{formatDate(selectedCase.estimated_completion_date)}</span>
                    </div>
                  </div>
                </div>

                {/* Stage Management */}
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    🔄 Stage Management
                  </h3>
                  <div className="space-y-4">
                    {selectedCase.tracker.map((stage) => {
                      const status = getStageStatus(stage);
                      const isNextStage = stage.stage_id === selectedCase.current_stage_id && !stage.completed;
                      
                      return (
                        <div key={stage.stage_id} className={`p-4 border rounded-lg ${status.bg}`}>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              <span className="text-xl">{status.icon}</span>
                              <div>
                                <h4 className={`font-medium ${status.color}`}>
                                  Stage {stage.stage_id}: {stage.name}
                                </h4>
                                {stage.date_completed && (
                                  <p className="text-sm text-gray-600">
                                    Completed: {formatDate(stage.date_completed)}
                                  </p>
                                )}
                                {stage.notes && (
                                  <p className="text-sm text-gray-600">
                                    Notes: {stage.notes}
                                  </p>
                                )}
                              </div>
                            </div>
                            {isNextStage && (
                              <button
                                onClick={() => markStageComplete(selectedCase.user_id, stage.stage_id)}
                                disabled={loading}
                                className="px-4 py-2 bg-green-600 text-white rounded text-sm font-medium hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50"
                              >
                                {loading ? 'Updating...' : 'Mark Complete'}
                              </button>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Next Step Info */}
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    🎯 Next Step Estimate
                  </h3>
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div className="flex items-center space-x-3">
                      <span className="text-2xl">📅</span>
                      <div>
                        <h4 className="font-medium text-blue-900">
                          {selectedCase.next_step_estimate.stage_name}
                        </h4>
                        <p className="text-sm text-blue-700">
                          Expected: {formatDate(selectedCase.next_step_estimate.expected_date)}
                        </p>
                        <p className="text-sm text-blue-700">
                          ETA: {selectedCase.next_step_estimate.eta_days} days
                        </p>
                        <p className="text-sm text-blue-700">
                          Confidence: {selectedCase.next_step_estimate.confidence_level}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-md p-8 text-center">
                <div className="text-6xl mb-4">📋</div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Select a Case
                </h3>
                <p className="text-gray-600">
                  Choose a case from the list to view details and manage stages
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}; 