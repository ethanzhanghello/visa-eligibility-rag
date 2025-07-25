import { TrackingStage, ProcessingTimeConfig } from '../types/tracking';

export const DEFAULT_STAGES: TrackingStage[] = [
  {
    stage_id: 1,
    name: 'Form I-130/I-140 Filed',
    description: 'Initial petition has been filed with USCIS',
    required_input: 'manual',
    estimated_duration_days: { min: 0, max: 0, average: 0 }, // Starting point
    is_milestone: true,
    requires_user_action: false
  },
  {
    stage_id: 2,
    name: 'USCIS Receipt Notice',
    description: 'USCIS has sent confirmation of receipt',
    required_input: 'auto',
    estimated_duration_days: { min: 7, max: 21, average: 14 },
    is_milestone: true,
    requires_user_action: false
  },
  {
    stage_id: 3,
    name: 'Biometrics Completed',
    description: 'Fingerprints and photos have been taken',
    required_input: 'manual',
    estimated_duration_days: { min: 21, max: 42, average: 28 },
    is_milestone: true,
    requires_user_action: true
  },
  {
    stage_id: 4,
    name: 'EAD/AP Issued',
    description: 'Employment Authorization and/or Advance Parole document issued',
    required_input: 'optional',
    estimated_duration_days: { min: 60, max: 120, average: 90 },
    is_milestone: false,
    requires_user_action: false
  },
  {
    stage_id: 5,
    name: 'Case Transferred',
    description: 'Case has been transferred between USCIS offices',
    required_input: 'auto',
    estimated_duration_days: { min: 7, max: 30, average: 14 },
    is_milestone: false,
    requires_user_action: false
  },
  {
    stage_id: 6,
    name: 'Interview Scheduled',
    description: 'Interview notice has been sent',
    required_input: 'manual',
    estimated_duration_days: { min: 90, max: 300, average: 180 },
    is_milestone: true,
    requires_user_action: false
  },
  {
    stage_id: 7,
    name: 'Interview Completed',
    description: 'Adjustment of status interview has been conducted',
    required_input: 'manual',
    estimated_duration_days: { min: 7, max: 60, average: 30 },
    is_milestone: true,
    requires_user_action: true
  },
  {
    stage_id: 8,
    name: 'Green Card Approved',
    description: 'Final approval decision has been made',
    required_input: 'manual',
    estimated_duration_days: { min: 7, max: 30, average: 14 },
    is_milestone: true,
    requires_user_action: false
  },
  {
    stage_id: 9,
    name: 'Green Card Produced',
    description: 'Physical green card has been produced',
    required_input: 'auto',
    estimated_duration_days: { min: 7, max: 21, average: 10 },
    is_milestone: false,
    requires_user_action: false
  },
  {
    stage_id: 10,
    name: 'Green Card Delivered',
    description: 'Physical green card has been delivered',
    required_input: 'auto',
    estimated_duration_days: { min: 3, max: 14, average: 7 },
    is_milestone: true,
    requires_user_action: false
  }
];

export const PROCESSING_TIME_CONFIGS: ProcessingTimeConfig[] = [
  {
    visa_type: 'EB-2',
    processing_center: 'California Service Center',
    country_specific_delays: {
      'China': 730, // ~2 years additional for China-born EB-2
      'India': 1095, // ~3 years additional for India-born EB-2
    },
    avg_durations_days: {
      '1_to_2': 14,   // Form filed to receipt notice
      '2_to_3': 28,   // Receipt to biometrics
      '3_to_4': 90,   // Biometrics to EAD/AP
      '3_to_5': 60,   // Biometrics to case transfer (if applicable)
      '5_to_6': 180,  // Case transfer to interview scheduled
      '6_to_7': 30,   // Interview scheduled to completed
      '7_to_8': 14,   // Interview to approval
      '8_to_9': 10,   // Approval to card production
      '9_to_10': 7    // Production to delivery
    },
    updated_at: '2024-01-01'
  },
  {
    visa_type: 'EB-1',
    processing_center: 'California Service Center',
    avg_durations_days: {
      '1_to_2': 14,
      '2_to_3': 28,
      '3_to_4': 90,
      '3_to_6': 120,  // EB-1 may skip case transfer
      '6_to_7': 30,
      '7_to_8': 14,
      '8_to_9': 10,
      '9_to_10': 7
    },
    updated_at: '2024-01-01'
  },
  {
    visa_type: 'EB-3',
    processing_center: 'California Service Center',
    country_specific_delays: {
      'China': 365,
      'India': 545,
      'Philippines': 180,
    },
    avg_durations_days: {
      '1_to_2': 14,
      '2_to_3': 35,
      '3_to_4': 120,
      '3_to_5': 45,
      '5_to_6': 210,
      '6_to_7': 45,
      '7_to_8': 21,
      '8_to_9': 14,
      '9_to_10': 7
    },
    updated_at: '2024-01-01'
  },
  // Add configurations for other centers
  {
    visa_type: 'EB-2',
    processing_center: 'Nebraska Service Center',
    country_specific_delays: {
      'China': 730,
      'India': 1095,
    },
    avg_durations_days: {
      '1_to_2': 10,
      '2_to_3': 21,
      '3_to_4': 75,
      '3_to_5': 45,
      '5_to_6': 150,
      '6_to_7': 25,
      '7_to_8': 10,
      '8_to_9': 7,
      '9_to_10': 5
    },
    updated_at: '2024-01-01'
  }
];

export const VISA_TYPE_OPTIONS = [
  { value: 'EB-1', label: 'EB-1 (Priority Workers)' },
  { value: 'EB-2', label: 'EB-2 (Advanced Degree/Exceptional Ability)' },
  { value: 'EB-3', label: 'EB-3 (Skilled Workers)' },
  { value: 'EB-4', label: 'EB-4 (Special Immigrants)' },
  { value: 'EB-5', label: 'EB-5 (Investors)' },
  { value: 'family-based', label: 'Family-Based' },
  { value: 'asylum', label: 'Asylum-Based' }
];

export const PROCESSING_CENTER_OPTIONS = [
  { value: 'California Service Center', label: 'California Service Center (CSC)' },
  { value: 'Nebraska Service Center', label: 'Nebraska Service Center (NSC)' },
  { value: 'Texas Service Center', label: 'Texas Service Center (TSC)' },
  { value: 'Vermont Service Center', label: 'Vermont Service Center (VSC)' },
  { value: 'Potomac Service Center', label: 'Potomac Service Center (PSC)' }
];

export const COUNTRY_OPTIONS = [
  { value: 'China', label: 'China' },
  { value: 'India', label: 'India' },
  { value: 'Philippines', label: 'Philippines' },
  { value: 'Mexico', label: 'Mexico' },
  { value: 'Vietnam', label: 'Vietnam' },
  { value: 'Other', label: 'Other Country' }
]; 