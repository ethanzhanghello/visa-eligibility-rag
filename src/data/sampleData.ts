import { CaseInfo, TimelineStep, Alert, DocumentResource, FAQ } from '../types';

export const sampleCaseInfo: CaseInfo = {
  category: 'EB-2 (Employment-Based)',
  priorityDate: 'March 5, 2021',
  uscisCenter: 'California Service Center',
  currentStep: 'Biometrics Completed',
  estimatedCompletion: '~September 2025',
  caseNumber: 'MSC2190012345',
  receipts: ['MSC2190012345', 'EAC2190054321']
};

export const sampleTimelineSteps: TimelineStep[] = [
  {
    id: 'petition_received',
    en: {
      title: 'Petition Received',
      description: 'USCIS has received your I-485 petition',
      tooltip: 'This is the first step in the adjustment of status process. USCIS has confirmed receipt of your application and supporting documents.'
    },
    zh: {
      title: '申请已收到',
      description: 'USCIS已收到您的I-485申请',
      tooltip: '这是身份调整过程的第一步。USCIS已确认收到您的申请和支持文件。'
    },
    status: 'completed',
    completedDate: '2023-03-15',
    processingTime: { min: 1, max: 2, average: 1 }
  },
  {
    id: 'biometrics',
    en: {
      title: 'Biometrics Appointment',
      description: 'Fingerprints and photos taken',
      tooltip: 'USCIS uses biometrics for background checks and to verify your identity.'
    },
    zh: {
      title: '生物识别预约',
      description: '已完成指纹和照片采集',
      tooltip: 'USCIS使用生物识别进行背景调查并验证您的身份。'
    },
    status: 'completed',
    completedDate: '2023-05-20',
    processingTime: { min: 2, max: 4, average: 3 }
  },
  {
    id: 'background_check',
    en: {
      title: 'Background Check',
      description: 'Security and background verification',
      tooltip: 'USCIS conducts thorough background checks including FBI name check, fingerprint check, and administrative check.'
    },
    zh: {
      title: '背景调查',
      description: '安全和背景验证',
      tooltip: 'USCIS进行全面的背景调查，包括FBI姓名检查、指纹检查和行政检查。'
    },
    status: 'in_progress',
    processingTime: { min: 2, max: 6, average: 4 }
  },
  {
    id: 'interview_scheduled',
    en: {
      title: 'Interview Scheduled',
      description: 'Interview notice sent',
      tooltip: 'You will receive an interview notice with the date, time, and location of your adjustment interview.'
    },
    zh: {
      title: '面试安排',
      description: '面试通知已发送',
      tooltip: '您将收到面试通知，包含面试的日期、时间和地点。'
    },
    status: 'pending',
    estimatedDate: '2024-01-15',
    processingTime: { min: 1, max: 3, average: 2 }
  },
  {
    id: 'interview_completed',
    en: {
      title: 'Interview Completed',
      description: 'Adjustment interview conducted',
      tooltip: 'During the interview, a USCIS officer will review your application and ask questions about your eligibility.'
    },
    zh: {
      title: '面试完成',
      description: '调整身份面试已进行',
      tooltip: '在面试期间，USCIS官员将审查您的申请并询问有关您资格的问题。'
    },
    status: 'pending',
    estimatedDate: '2024-02-01',
    processingTime: { min: 0, max: 1, average: 0 }
  },
  {
    id: 'decision',
    en: {
      title: 'Final Decision',
      description: 'Case decision made',
      tooltip: 'USCIS will make a final decision on your case and notify you of the outcome.'
    },
    zh: {
      title: '最终决定',
      description: '案件决定已做出',
      tooltip: 'USCIS将对您的案件做出最终决定并通知您结果。'
    },
    status: 'pending',
    estimatedDate: '2024-03-15',
    processingTime: { min: 1, max: 2, average: 1 }
  },
  {
    id: 'green_card_issued',
    en: {
      title: 'Green Card Issued',
      description: 'Physical green card produced and mailed',
      tooltip: 'Your physical green card will be produced and mailed to the address on file.'
    },
    zh: {
      title: '绿卡发放',
      description: '实体绿卡制作并邮寄',
      tooltip: '您的实体绿卡将被制作并邮寄到您的登记地址。'
    },
    status: 'pending',
    estimatedDate: '2024-04-01',
    processingTime: { min: 1, max: 2, average: 1 }
  }
];

export const sampleAlerts: Alert[] = [
  {
    id: 'visa_bulletin_update',
    type: 'update',
    en: {
      title: 'Visa Bulletin Update',
      message: 'Your priority date is now current! This means your case can move forward in processing.'
    },
    zh: {
      title: '签证公告更新',
      message: '您的优先日期现在是当前的！这意味着您的案件可以继续处理。'
    },
    timestamp: '2023-11-01T10:00:00Z',
    isRead: false,
    actionRequired: false
  },
  {
    id: 'processing_time_update',
    type: 'info',
    en: {
      title: 'Processing Time Update',
      message: 'Your processing center posted new estimated times (CSC: 14 months → 13.5 months)'
    },
    zh: {
      title: '处理时间更新',
      message: '您的处理中心发布了新的预估时间（CSC：14个月 → 13.5个月）'
    },
    timestamp: '2023-10-28T14:30:00Z',
    isRead: false,
    actionRequired: false
  },
  {
    id: 'document_reminder',
    type: 'reminder',
    en: {
      title: 'Document Preparation Reminder',
      message: 'Consider starting your medical examination preparation as your interview may be scheduled soon.'
    },
    zh: {
      title: '文件准备提醒',
      message: '考虑开始准备您的体检，因为您的面试可能很快就会安排。'
    },
    timestamp: '2023-10-25T09:00:00Z',
    isRead: true,
    actionRequired: true
  }
];

export const sampleDocuments: DocumentResource[] = [
  {
    id: 'interview_checklist',
    en: {
      title: 'Interview Document Checklist',
      description: 'Complete list of documents required for your adjustment of status interview',
      url: '/documents/interview_checklist_en.pdf'
    },
    zh: {
      title: '面试文件清单',
      description: '调整身份面试所需文件的完整列表',
      url: '/documents/interview_checklist_zh.pdf'
    },
    category: 'checklist',
    relevantSteps: ['interview_scheduled', 'interview_completed']
  },
  {
    id: 'medical_exam_guide',
    en: {
      title: 'Medical Examination Guide (I-693)',
      description: 'Instructions for completing the medical examination with a civil surgeon',
      url: '/documents/medical_exam_guide_en.pdf'
    },
    zh: {
      title: '体检指南 (I-693)',
      description: '在民事外科医生处完成体检的说明',
      url: '/documents/medical_exam_guide_zh.pdf'
    },
    category: 'guide',
    relevantSteps: ['interview_scheduled']
  },
  {
    id: 'employment_letter_template',
    en: {
      title: 'Employment Verification Letter Template',
      description: 'Template for requesting an employment verification letter from your employer',
    },
    zh: {
      title: '就业证明信模板',
      description: '向雇主申请就业证明信的模板',
    },
    category: 'form',
    relevantSteps: ['interview_scheduled', 'interview_completed']
  }
];

export const sampleFAQs: FAQ[] = [
  {
    id: 'lost_documents',
    en: {
      question: 'How do I know if USCIS lost my documents?',
      answer: 'If your case has been pending longer than normal processing times without updates, you can submit a case inquiry through the USCIS website or contact their customer service line. USCIS will investigate and may request you to resubmit documents if needed.'
    },
    zh: {
      question: '如何知道USCIS是否丢失了我的文件？',
      answer: '如果您的案件超过正常处理时间仍未有更新，您可以通过USCIS网站提交案件查询或联系他们的客服热线。USCIS将进行调查，如有需要可能会要求您重新提交文件。'
    },
    category: 'general',
    relevantSteps: ['background_check', 'interview_scheduled']
  },
  {
    id: 'medical_exam_timing',
    en: {
      question: 'When should I take the medical exam?',
      answer: 'You should complete your medical exam (Form I-693) after receiving your interview notice but before your interview date. The civil surgeon must complete the examination no more than 60 days before you submit it to USCIS, and the exam is valid for up to 2 years.'
    },
    zh: {
      question: '我什么时候应该进行体检？',
      answer: '您应该在收到面试通知后但在面试日期之前完成体检（表格I-693）。民事外科医生必须在您向USCIS提交体检报告前60天内完成检查，体检报告有效期最长为2年。'
    },
    category: 'medical',
    relevantSteps: ['interview_scheduled']
  },
  {
    id: 'interview_preparation',
    en: {
      question: 'How should I prepare for my green card interview?',
      answer: 'Review all documents in your case file, practice answering common interview questions, bring original documents and photocopies, arrive early, and dress professionally. Be honest and answer only what is asked.'
    },
    zh: {
      question: '我应该如何准备绿卡面试？',
      answer: '审查您案件文件中的所有文件，练习回答常见面试问题，携带原始文件和复印件，提前到达，着装专业。要诚实并只回答所问的问题。'
    },
    category: 'interview',
    relevantSteps: ['interview_scheduled', 'interview_completed']
  }
]; 