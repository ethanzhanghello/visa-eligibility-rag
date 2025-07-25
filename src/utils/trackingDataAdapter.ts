import { UserCaseTracker, StageProgress } from '../types/tracking';
import { CaseInfo, TimelineStep, Alert } from '../types';
import { DEFAULT_STAGES } from '../data/trackingConfig';

/**
 * Convert UserCaseTracker to Dashboard CaseInfo format
 */
export function convertToCaseInfo(trackingCase: UserCaseTracker): CaseInfo {
  const currentStage = DEFAULT_STAGES.find(s => s.stage_id === trackingCase.current_stage_id);
  
  return {
    category: trackingCase.visa_type,
    priorityDate: formatDate(trackingCase.priority_date),
    uscisCenter: trackingCase.processing_center,
    currentStep: currentStage?.name || `Stage ${trackingCase.current_stage_id}`,
    estimatedCompletion: formatDate(trackingCase.estimated_completion_date),
    caseNumber: trackingCase.case_number,
    receipts: trackingCase.case_number ? [trackingCase.case_number] : undefined
  };
}

/**
 * Convert UserCaseTracker to Dashboard TimelineStep format
 */
export function convertToTimelineSteps(trackingCase: UserCaseTracker): TimelineStep[] {
  return trackingCase.tracker.map(stage => {
    const stageConfig = DEFAULT_STAGES.find(s => s.stage_id === stage.stage_id);
    const status = getTimelineStatus(stage, trackingCase.current_stage_id);
    
    return {
      id: `stage_${stage.stage_id}`,
      en: {
        title: stage.name,
        description: stageConfig?.description || '',
        tooltip: generateTooltip(stage, stageConfig, 'en')
      },
      zh: {
        title: translateStageTitle(stage.name),
        description: translateStageDescription(stageConfig?.description || ''),
        tooltip: generateTooltip(stage, stageConfig, 'zh')
      },
      status: status,
      completedDate: stage.date_completed,
      estimatedDate: stage.date_estimated,
      processingTime: stageConfig ? {
        min: stageConfig.estimated_duration_days.min,
        max: stageConfig.estimated_duration_days.max,
        average: stageConfig.estimated_duration_days.average
      } : undefined
    };
  });
}

/**
 * Generate alerts based on tracking case status
 */
export function generateAlertsFromTracking(trackingCase: UserCaseTracker): Alert[] {
  const alerts: Alert[] = [];
  const currentDate = new Date();
  
  // Next step alert
  const nextStep = trackingCase.next_step_estimate;
  const expectedDate = new Date(nextStep.expected_date);
  const daysUntilNext = Math.ceil((expectedDate.getTime() - currentDate.getTime()) / (1000 * 60 * 60 * 24));
  
  if (daysUntilNext <= 30 && daysUntilNext > 0) {
    alerts.push({
      id: 'next_step_soon',
      type: 'info',
      en: {
        title: 'Next Step Approaching',
        message: `Your next step "${nextStep.stage_name}" is expected in ${daysUntilNext} days.`
      },
      zh: {
        title: '下一步即将到来',
        message: `您的下一步"${translateStageTitle(nextStep.stage_name)}"预计在${daysUntilNext}天内进行。`
      },
      timestamp: new Date().toISOString(),
      isRead: false,
      actionRequired: false
    });
  }
  
  // EAD expiration alert
  if (trackingCase.has_ead_application) {
    const eadStage = trackingCase.tracker.find(s => s.stage_id === 4);
    if (eadStage?.completed && eadStage.date_completed) {
      const eadDate = new Date(eadStage.date_completed);
      const expirationDate = new Date(eadDate);
      expirationDate.setFullYear(expirationDate.getFullYear() + 1); // EAD valid for 1 year
      
      const daysUntilExpiration = Math.ceil((expirationDate.getTime() - currentDate.getTime()) / (1000 * 60 * 60 * 24));
      
      if (daysUntilExpiration <= 90 && daysUntilExpiration > 0) {
        alerts.push({
          id: 'ead_expiring',
          type: 'warning',
          en: {
            title: 'EAD Expiring Soon',
            message: `Your Employment Authorization Document expires in ${daysUntilExpiration} days. Consider filing for renewal.`
          },
          zh: {
            title: 'EAD即将到期',
            message: `您的工作许可证将在${daysUntilExpiration}天后到期。请考虑申请续期。`
          },
          timestamp: new Date().toISOString(),
          isRead: false,
          actionRequired: true
        });
      }
    }
  }
  
  // Interview preparation alert
  const interviewStage = trackingCase.tracker.find(s => s.stage_id === 6);
  if (interviewStage && !interviewStage.completed && interviewStage.date_estimated) {
    const interviewDate = new Date(interviewStage.date_estimated);
    const daysUntilInterview = Math.ceil((interviewDate.getTime() - currentDate.getTime()) / (1000 * 60 * 60 * 24));
    
    if (daysUntilInterview <= 60 && daysUntilInterview > 0) {
      alerts.push({
        id: 'interview_prep',
        type: 'reminder',
        en: {
          title: 'Interview Preparation',
          message: `Your interview is estimated in ${daysUntilInterview} days. Start preparing your documents and practice common questions.`
        },
        zh: {
          title: '面试准备',
          message: `您的面试预计在${daysUntilInterview}天后进行。请开始准备您的文件并练习常见问题。`
        },
        timestamp: new Date().toISOString(),
        isRead: false,
        actionRequired: true
      });
    }
  }
  
  return alerts;
}

/**
 * Helper function to determine timeline status
 */
function getTimelineStatus(stage: StageProgress, currentStageId: number): 'completed' | 'in_progress' | 'pending' | 'estimated' {
  if (stage.completed) {
    return 'completed';
  } else if (stage.stage_id === currentStageId) {
    return 'in_progress';
  } else if (stage.stage_id < currentStageId) {
    return 'completed'; // Should not happen, but handle gracefully
  } else {
    return 'pending';
  }
}

/**
 * Generate tooltip text for timeline steps
 */
function generateTooltip(stage: StageProgress, stageConfig: any, language: 'en' | 'zh'): string {
  const base = stageConfig?.description || '';
  
  if (stage.completed && stage.date_completed) {
    const completedText = language === 'zh' ? 
      `完成于 ${formatDate(stage.date_completed)}` : 
      `Completed on ${formatDate(stage.date_completed)}`;
    return `${base}\n\n${completedText}`;
  } else if (stage.date_estimated) {
    const estimatedText = language === 'zh' ? 
      `预计 ${formatDate(stage.date_estimated)}` : 
      `Estimated ${formatDate(stage.date_estimated)}`;
    return `${base}\n\n${estimatedText}`;
  }
  
  return base;
}

/**
 * Format date string for display
 */
function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

/**
 * Translate stage titles to Chinese (simplified mapping)
 */
function translateStageTitle(title: string): string {
  const translations: Record<string, string> = {
    'Form I-130/I-140 Filed': '表格 I-130/I-140 已提交',
    'USCIS Receipt Notice': 'USCIS 收据通知',
    'Biometrics Completed': '生物识别已完成',
    'EAD/AP Issued': 'EAD/AP 已发放',
    'Case Transferred': '案件已转移',
    'Interview Scheduled': '面试已安排',
    'Interview Completed': '面试已完成',
    'Green Card Approved': '绿卡已批准',
    'Green Card Produced': '绿卡已制作',
    'Green Card Delivered': '绿卡已送达'
  };
  
  return translations[title] || title;
}

/**
 * Translate stage descriptions to Chinese (simplified mapping)
 */
function translateStageDescription(description: string): string {
  // In a real implementation, this would use a proper translation service
  const translations: Record<string, string> = {
    'Initial petition has been filed with USCIS': '初始申请已向 USCIS 提交',
    'USCIS has sent confirmation of receipt': 'USCIS 已发送收据确认',
    'Fingerprints and photos have been taken': '已采集指纹和照片',
    'Employment Authorization and/or Advance Parole document issued': '工作许可和/或提前假释文件已发放',
    'Case has been transferred between USCIS offices': '案件已在 USCIS 办公室之间转移',
    'Interview notice has been sent': '面试通知已发送',
    'Adjustment of status interview has been conducted': '身份调整面试已进行',
    'Final approval decision has been made': '最终批准决定已做出',
    'Physical green card has been produced': '实体绿卡已制作',
    'Physical green card has been delivered': '实体绿卡已送达'
  };
  
  return translations[description] || description;
} 