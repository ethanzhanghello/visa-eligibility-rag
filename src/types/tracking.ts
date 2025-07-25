// Green Card Case Tracking System Types

export interface TrackingStage {
  stage_id: number;
  name: string;
  description: string;
  required_input: 'manual' | 'auto' | 'optional';
  estimated_duration_days: {
    min: number;
    max: number;
    average: number;
  };
  is_milestone: boolean;
  requires_user_action: boolean;
}

export interface StageProgress {
  stage_id: number;
  name: string;
  completed: boolean;
  date_completed?: string;
  date_estimated?: string;
  notes?: string;
  updated_by?: string; // admin user ID who marked it complete
  updated_at?: string;
}

export interface NextStepEstimate {
  stage_id: number;
  stage_name: string;
  eta_days: number;
  expected_date: string;
  confidence_level: 'high' | 'medium' | 'low';
}

export interface UserCaseTracker {
  user_id: string;
  case_number?: string;
  visa_type: 'EB-1' | 'EB-2' | 'EB-3' | 'EB-4' | 'EB-5' | 'family-based' | 'asylum';
  priority_date: string;
  processing_center: 'California Service Center' | 'Nebraska Service Center' | 'Texas Service Center' | 'Vermont Service Center' | 'Potomac Service Center';
  country_of_birth: string;
  created_at: string;
  updated_at: string;
  
  // Progress tracking
  tracker: StageProgress[];
  current_stage_id: number;
  estimated_completion_date: string;
  next_step_estimate: NextStepEstimate;
  
  // Additional metadata
  is_concurrent_filing: boolean;
  has_ead_application: boolean;
  has_ap_application: boolean;
  attorney_info?: {
    name: string;
    firm: string;
    email: string;
  };
}

export interface ProcessingTimeConfig {
  visa_type: string;
  processing_center: string;
  country_specific_delays?: {
    [country: string]: number; // additional days
  };
  avg_durations_days: {
    [transition: string]: number; // e.g., "1_to_2": 10
  };
  updated_at: string;
}

export interface CaseUpdate {
  case_id: string;
  stage_id: number;
  action: 'complete' | 'update_estimate' | 'add_note';
  data: {
    date_completed?: string;
    estimated_date?: string;
    notes?: string;
  };
  admin_user_id: string;
  timestamp: string;
}

export interface AdminDashboardData {
  total_cases: number;
  cases_by_stage: {
    [stage_id: number]: number;
  };
  recent_updates: CaseUpdate[];
  pending_actions: {
    stage_id: number;
    count: number;
  }[];
}

export interface TrackingSystemConfig {
  stages: TrackingStage[];
  processing_times: ProcessingTimeConfig[];
  notification_triggers: {
    stage_id: number;
    days_before_estimate: number;
    message_template: string;
  }[];
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  timestamp: string;
}

export interface CaseListResponse {
  cases: UserCaseTracker[];
  total: number;
  page: number;
  limit: number;
}

export interface StageUpdateRequest {
  case_id: string;
  stage_id: number;
  completed: boolean;
  date_completed?: string;
  notes?: string;
}

export interface EstimationRequest {
  visa_type: string;
  processing_center: string;
  country_of_birth: string;
  current_stage_id: number;
  completed_stages: StageProgress[];
} 