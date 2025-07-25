import { UserCaseTracker } from '../types/tracking';
import { EstimationEngine } from '../utils/estimationEngine';

// Sample user tracking data
export const sampleTrackingCase: UserCaseTracker = {
  user_id: 'user123',
  case_number: 'MSC2490012345',
  visa_type: 'EB-2',
  priority_date: '2021-03-05',
  processing_center: 'California Service Center',
  country_of_birth: 'China',
  created_at: '2024-03-01T00:00:00Z',
  updated_at: '2024-11-01T15:30:00Z',
  current_stage_id: 3,
  estimated_completion_date: '2025-09-15',
  next_step_estimate: {
    stage_id: 4,
    stage_name: 'EAD/AP Issued',
    eta_days: 90,
    expected_date: '2024-12-01',
    confidence_level: 'medium'
  },
  is_concurrent_filing: true,
  has_ead_application: true,
  has_ap_application: true,
  attorney_info: {
    name: 'Jane Smith',
    firm: 'Smith Immigration Law',
    email: 'jane@smithlaw.com'
  },
  tracker: [
    {
      stage_id: 1,
      name: 'Form I-130/I-140 Filed',
      completed: true,
      date_completed: '2024-03-01',
      notes: 'EB-2 petition filed with concurrent I-485',
      updated_by: 'admin',
      updated_at: '2024-03-01T10:00:00Z'
    },
    {
      stage_id: 2,
      name: 'USCIS Receipt Notice',
      completed: true,
      date_completed: '2024-03-15',
      notes: 'Receipt notice received for all forms',
      updated_by: 'admin',
      updated_at: '2024-03-15T14:20:00Z'
    },
    {
      stage_id: 3,
      name: 'Biometrics Completed',
      completed: true,
      date_completed: '2024-04-10',
      notes: 'Biometrics appointment completed at ASC',
      updated_by: 'admin',
      updated_at: '2024-04-10T16:45:00Z'
    },
    {
      stage_id: 4,
      name: 'EAD/AP Issued',
      completed: false,
      date_estimated: '2024-12-01',
      notes: 'EAD application under review'
    },
    {
      stage_id: 5,
      name: 'Case Transferred',
      completed: false,
      date_estimated: '2024-12-15'
    },
    {
      stage_id: 6,
      name: 'Interview Scheduled',
      completed: false,
      date_estimated: '2025-06-01'
    },
    {
      stage_id: 7,
      name: 'Interview Completed',
      completed: false,
      date_estimated: '2025-07-01'
    },
    {
      stage_id: 8,
      name: 'Green Card Approved',
      completed: false,
      date_estimated: '2025-08-01'
    },
    {
      stage_id: 9,
      name: 'Green Card Produced',
      completed: false,
      date_estimated: '2025-08-15'
    },
    {
      stage_id: 10,
      name: 'Green Card Delivered',
      completed: false,
      date_estimated: '2025-09-01'
    }
  ]
};

// Additional sample cases for admin portal
export const sampleTrackingCases: UserCaseTracker[] = [
  sampleTrackingCase,
  
  // EB-1 Case - Further along
  {
    user_id: 'user456',
    case_number: 'MSC2490067890',
    visa_type: 'EB-1',
    priority_date: '2023-01-15',
    processing_center: 'Nebraska Service Center',
    country_of_birth: 'India',
    created_at: '2023-01-15T00:00:00Z',
    updated_at: '2024-10-15T12:00:00Z',
    current_stage_id: 7,
    estimated_completion_date: '2024-12-15',
    next_step_estimate: {
      stage_id: 8,
      stage_name: 'Green Card Approved',
      eta_days: 14,
      expected_date: '2024-11-15',
      confidence_level: 'high'
    },
    is_concurrent_filing: true,
    has_ead_application: false,
    has_ap_application: true,
    tracker: [
      {
        stage_id: 1,
        name: 'Form I-130/I-140 Filed',
        completed: true,
        date_completed: '2023-01-15',
        updated_by: 'admin'
      },
      {
        stage_id: 2,
        name: 'USCIS Receipt Notice',
        completed: true,
        date_completed: '2023-01-28',
        updated_by: 'admin'
      },
      {
        stage_id: 3,
        name: 'Biometrics Completed',
        completed: true,
        date_completed: '2023-03-10',
        updated_by: 'admin'
      },
      {
        stage_id: 4,
        name: 'EAD/AP Issued',
        completed: true,
        date_completed: '2023-06-01',
        updated_by: 'admin'
      },
      {
        stage_id: 5,
        name: 'Case Transferred',
        completed: true,
        date_completed: '2023-08-15',
        updated_by: 'admin'
      },
      {
        stage_id: 6,
        name: 'Interview Scheduled',
        completed: true,
        date_completed: '2024-09-01',
        updated_by: 'admin'
      },
      {
        stage_id: 7,
        name: 'Interview Completed',
        completed: true,
        date_completed: '2024-10-15',
        notes: 'Interview successful, approval recommended',
        updated_by: 'admin'
      },
      {
        stage_id: 8,
        name: 'Green Card Approved',
        completed: false,
        date_estimated: '2024-11-15'
      },
      {
        stage_id: 9,
        name: 'Green Card Produced',
        completed: false,
        date_estimated: '2024-11-25'
      },
      {
        stage_id: 10,
        name: 'Green Card Delivered',
        completed: false,
        date_estimated: '2024-12-05'
      }
    ]
  },

  // EB-3 Case - Early stage
  {
    user_id: 'user789',
    case_number: 'MSC2490098765',
    visa_type: 'EB-3',
    priority_date: '2024-08-01',
    processing_center: 'Texas Service Center',
    country_of_birth: 'Philippines',
    created_at: '2024-08-01T00:00:00Z',
    updated_at: '2024-10-01T09:30:00Z',
    current_stage_id: 2,
    estimated_completion_date: '2026-05-15',
    next_step_estimate: {
      stage_id: 3,
      stage_name: 'Biometrics Completed',
      eta_days: 35,
      expected_date: '2024-11-15',
      confidence_level: 'high'
    },
    is_concurrent_filing: false,
    has_ead_application: false,
    has_ap_application: false,
    tracker: [
      {
        stage_id: 1,
        name: 'Form I-130/I-140 Filed',
        completed: true,
        date_completed: '2024-08-01',
        updated_by: 'admin'
      },
      {
        stage_id: 2,
        name: 'USCIS Receipt Notice',
        completed: true,
        date_completed: '2024-08-15',
        updated_by: 'admin'
      },
      {
        stage_id: 3,
        name: 'Biometrics Completed',
        completed: false,
        date_estimated: '2024-11-15'
      },
      {
        stage_id: 4,
        name: 'EAD/AP Issued',
        completed: false,
        date_estimated: '2025-02-15'
      },
      {
        stage_id: 5,
        name: 'Case Transferred',
        completed: false,
        date_estimated: '2025-04-01'
      },
      {
        stage_id: 6,
        name: 'Interview Scheduled',
        completed: false,
        date_estimated: '2026-01-15'
      },
      {
        stage_id: 7,
        name: 'Interview Completed',
        completed: false,
        date_estimated: '2026-03-01'
      },
      {
        stage_id: 8,
        name: 'Green Card Approved',
        completed: false,
        date_estimated: '2026-04-01'
      },
      {
        stage_id: 9,
        name: 'Green Card Produced',
        completed: false,
        date_estimated: '2026-04-15'
      },
      {
        stage_id: 10,
        name: 'Green Card Delivered',
        completed: false,
        date_estimated: '2026-05-01'
      }
    ]
  }
];

// Initialize cases if not already present (for demo)
export const initializeSampleCases = () => {
  // This would typically be handled by the API/database
  // For demo purposes, we can use this to populate initial data
  return sampleTrackingCases;
}; 