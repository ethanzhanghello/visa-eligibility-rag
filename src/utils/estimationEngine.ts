import { 
  UserCaseTracker, 
  StageProgress, 
  NextStepEstimate, 
  ProcessingTimeConfig,
  TrackingStage 
} from '../types/tracking';
import { DEFAULT_STAGES, PROCESSING_TIME_CONFIGS } from '../data/trackingConfig';

export class EstimationEngine {
  private stages: TrackingStage[];
  private processingTimes: ProcessingTimeConfig[];

  constructor() {
    this.stages = DEFAULT_STAGES;
    this.processingTimes = PROCESSING_TIME_CONFIGS;
  }

  /**
   * Calculate the next step estimate for a user's case
   */
  calculateNextStep(caseData: UserCaseTracker): NextStepEstimate {
    const currentStage = caseData.current_stage_id;
    const nextStage = this.getNextStage(currentStage);
    
    if (!nextStage) {
      // Case is complete
      return {
        stage_id: currentStage,
        stage_name: 'Case Complete',
        eta_days: 0,
        expected_date: new Date().toISOString().split('T')[0],
        confidence_level: 'high'
      };
    }

    const config = this.getProcessingConfig(caseData.visa_type, caseData.processing_center);
    const transitionKey = `${currentStage}_to_${nextStage.stage_id}`;
    const baseDays = config?.avg_durations_days[transitionKey] || nextStage.estimated_duration_days.average;
    
    // Apply country-specific delays
    const countryDelay = this.getCountryDelay(config, caseData.country_of_birth, nextStage.stage_id);
    const totalDays = baseDays + countryDelay;
    
    // Calculate expected date from the last completed stage
    const lastCompletedDate = this.getLastCompletedDate(caseData.tracker);
    const expectedDate = this.addDaysToDate(lastCompletedDate, totalDays);
    
    // Determine confidence level based on historical accuracy
    const confidenceLevel = this.calculateConfidence(caseData, nextStage.stage_id);

    return {
      stage_id: nextStage.stage_id,
      stage_name: nextStage.name,
      eta_days: totalDays,
      expected_date: expectedDate,
      confidence_level: confidenceLevel
    };
  }

  /**
   * Calculate the estimated completion date for the entire case
   */
  calculateCompletionDate(caseData: UserCaseTracker): string {
    const currentStage = caseData.current_stage_id;
    const remainingStages = this.getRemainingStages(currentStage);
    const config = this.getProcessingConfig(caseData.visa_type, caseData.processing_center);
    
    let totalRemainingDays = 0;
    let previousStageId = currentStage;

    for (const stage of remainingStages) {
      const transitionKey = `${previousStageId}_to_${stage.stage_id}`;
      const baseDays = config?.avg_durations_days[transitionKey] || stage.estimated_duration_days.average;
      const countryDelay = this.getCountryDelay(config, caseData.country_of_birth, stage.stage_id);
      
      totalRemainingDays += baseDays + countryDelay;
      previousStageId = stage.stage_id;
    }

    const lastCompletedDate = this.getLastCompletedDate(caseData.tracker);
    return this.addDaysToDate(lastCompletedDate, totalRemainingDays);
  }

  /**
   * Update case estimates when a stage is marked complete
   */
  updateCaseEstimates(caseData: UserCaseTracker, completedStageId: number, completionDate: string): Partial<UserCaseTracker> {
    // Update the stage as completed
    const updatedTracker = caseData.tracker.map(stage => 
      stage.stage_id === completedStageId 
        ? { ...stage, completed: true, date_completed: completionDate }
        : stage
    );

    // Update current stage
    const newCurrentStage = this.getNextStageId(completedStageId) || completedStageId;
    
    // Create updated case data
    const updatedCase: UserCaseTracker = {
      ...caseData,
      tracker: updatedTracker,
      current_stage_id: newCurrentStage,
      updated_at: new Date().toISOString()
    };

    // Recalculate estimates
    const nextStep = this.calculateNextStep(updatedCase);
    const completionDate = this.calculateCompletionDate(updatedCase);

    return {
      tracker: updatedTracker,
      current_stage_id: newCurrentStage,
      next_step_estimate: nextStep,
      estimated_completion_date: completionDate,
      updated_at: new Date().toISOString()
    };
  }

  /**
   * Get processing configuration for specific visa type and center
   */
  private getProcessingConfig(visaType: string, processingCenter: string): ProcessingTimeConfig | undefined {
    return this.processingTimes.find(config => 
      config.visa_type === visaType && config.processing_center === processingCenter
    );
  }

  /**
   * Get country-specific delay for a stage
   */
  private getCountryDelay(config: ProcessingTimeConfig | undefined, country: string, stageId: number): number {
    if (!config?.country_specific_delays || !config.country_specific_delays[country]) {
      return 0;
    }

    // Apply country delays primarily to interview scheduling (stage 6)
    if (stageId === 6) {
      return config.country_specific_delays[country];
    }

    return 0;
  }

  /**
   * Get the next stage in the process
   */
  private getNextStage(currentStageId: number): TrackingStage | undefined {
    return this.stages.find(stage => stage.stage_id === currentStageId + 1);
  }

  /**
   * Get the next stage ID
   */
  private getNextStageId(currentStageId: number): number | undefined {
    const nextStage = this.getNextStage(currentStageId);
    return nextStage?.stage_id;
  }

  /**
   * Get all remaining stages after current stage
   */
  private getRemainingStages(currentStageId: number): TrackingStage[] {
    return this.stages.filter(stage => stage.stage_id > currentStageId);
  }

  /**
   * Get the date of the last completed stage
   */
  private getLastCompletedDate(tracker: StageProgress[]): string {
    const completedStages = tracker
      .filter(stage => stage.completed && stage.date_completed)
      .sort((a, b) => a.stage_id - b.stage_id);
    
    return completedStages.length > 0 
      ? completedStages[completedStages.length - 1].date_completed!
      : new Date().toISOString().split('T')[0];
  }

  /**
   * Add days to a date string and return new date string
   */
  private addDaysToDate(dateString: string, days: number): string {
    const date = new Date(dateString);
    date.setDate(date.getDate() + days);
    return date.toISOString().split('T')[0];
  }

  /**
   * Calculate confidence level based on historical data and case characteristics
   */
  private calculateConfidence(caseData: UserCaseTracker, nextStageId: number): 'high' | 'medium' | 'low' {
    // High confidence for early stages and standard processing centers
    if (nextStageId <= 3) return 'high';
    
    // Medium confidence for mid-process stages
    if (nextStageId <= 6) return 'medium';
    
    // Lower confidence for later stages, especially with country delays
    const hasCountryDelay = ['China', 'India', 'Philippines'].includes(caseData.country_of_birth);
    return hasCountryDelay ? 'low' : 'medium';
  }

  /**
   * Initialize a new case tracker
   */
  static initializeCase(
    userId: string, 
    visaType: string, 
    processingCenter: string, 
    priorityDate: string,
    countryOfBirth: string
  ): UserCaseTracker {
    const engine = new EstimationEngine();
    
    // Initialize all stages as not completed
    const tracker: StageProgress[] = engine.stages.map(stage => ({
      stage_id: stage.stage_id,
      name: stage.name,
      completed: false,
      date_estimated: stage.stage_id === 1 ? new Date().toISOString().split('T')[0] : undefined
    }));

    const caseData: UserCaseTracker = {
      user_id: userId,
      visa_type: visaType as any,
      processing_center: processingCenter as any,
      priority_date: priorityDate,
      country_of_birth: countryOfBirth,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      tracker,
      current_stage_id: 1,
      estimated_completion_date: '',
      next_step_estimate: {
        stage_id: 1,
        stage_name: 'Form I-130/I-140 Filed',
        eta_days: 0,
        expected_date: new Date().toISOString().split('T')[0],
        confidence_level: 'high'
      },
      is_concurrent_filing: false,
      has_ead_application: false,
      has_ap_application: false
    };

    // Calculate initial estimates
    caseData.next_step_estimate = engine.calculateNextStep(caseData);
    caseData.estimated_completion_date = engine.calculateCompletionDate(caseData);

    return caseData;
  }
} 