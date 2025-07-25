import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { CaseInfo } from '../types';

interface UserComparisonProps {
  caseInfo: CaseInfo;
  currentLanguage: string;
}

interface ComparisonData {
  category: string;
  userPercentile: number;
  averageTimeToCurrentStage: number;
  userTimeToCurrentStage: number;
  estimatedVsAverage: number;
  similarCasesCount: number;
}

export const UserComparisonWidget: React.FC<UserComparisonProps> = ({
  caseInfo,
  currentLanguage
}) => {
  const { t } = useTranslation();
  const [comparisonData, setComparisonData] = useState<ComparisonData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate fetching comparison data
    setTimeout(() => {
      const mockData: ComparisonData = {
        category: caseInfo.category,
        userPercentile: Math.floor(Math.random() * 40) + 60, // 60-100% (ahead of others)
        averageTimeToCurrentStage: 8, // months
        userTimeToCurrentStage: 6, // months (faster than average)
        estimatedVsAverage: -3, // 3 months faster than average
        similarCasesCount: Math.floor(Math.random() * 500) + 200
      };
      setComparisonData(mockData);
      setLoading(false);
    }, 1000);
  }, [caseInfo]);

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div className="space-y-3">
            <div className="h-3 bg-gray-200 rounded"></div>
            <div className="h-3 bg-gray-200 rounded w-5/6"></div>
            <div className="h-3 bg-gray-200 rounded w-4/6"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!comparisonData) return null;

  const getPercentileColor = (percentile: number): string => {
    if (percentile >= 80) return 'text-green-600 bg-green-50';
    if (percentile >= 60) return 'text-blue-600 bg-blue-50';
    if (percentile >= 40) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  const getPercentileMessage = (percentile: number): string => {
    if (currentLanguage === 'zh') {
      if (percentile >= 80) return '您的进度非常快！';
      if (percentile >= 60) return '您的进度良好';
      if (percentile >= 40) return '您的进度正常';
      return '您的进度稍慢';
    } else {
      if (percentile >= 80) return 'Excellent progress!';
      if (percentile >= 60) return 'Good progress';
      if (percentile >= 40) return 'Average progress';
      return 'Below average progress';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">
          📈 {t('caseComparison', 'Case Comparison')}
        </h3>
        <span className="text-xs text-gray-500">
          {t('anonymizedData', 'Anonymized data')}
        </span>
      </div>

      {/* Main Percentile Display */}
      <div className={`p-4 rounded-lg mb-4 ${getPercentileColor(comparisonData.userPercentile)}`}>
        <div className="text-center">
          <div className="text-3xl font-bold mb-2">
            {comparisonData.userPercentile}%
          </div>
          <div className="text-sm font-medium">
            {currentLanguage === 'zh' 
              ? `您的进度快于 ${comparisonData.userPercentile}% 的同类申请人`
              : `You're ahead of ${comparisonData.userPercentile}% of similar ${comparisonData.category} applicants`
            }
          </div>
          <div className="text-xs mt-1">
            {getPercentileMessage(comparisonData.userPercentile)}
          </div>
        </div>
      </div>

      {/* Detailed Comparisons */}
      <div className="space-y-4">
        {/* Time to Current Stage */}
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
          <div>
            <div className="text-sm font-medium text-gray-900">
              {t('timeToCurrentStage', 'Time to Current Stage')}
            </div>
            <div className="text-xs text-gray-600">
              {t('vsAverageApplicant', 'vs. average applicant')}
            </div>
          </div>
          <div className="text-right">
            <div className="text-lg font-semibold text-gray-900">
              {comparisonData.userTimeToCurrentStage}m
            </div>
            <div className="text-xs text-gray-500">
              {t('avg', 'Avg')}: {comparisonData.averageTimeToCurrentStage}m
            </div>
          </div>
        </div>

        {/* Estimated Completion vs Average */}
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
          <div>
            <div className="text-sm font-medium text-gray-900">
              {t('estimatedCompletion', 'Estimated Completion')}
            </div>
            <div className="text-xs text-gray-600">
              {t('comparedToAverage', 'compared to average')}
            </div>
          </div>
          <div className="text-right">
            <div className={`text-lg font-semibold ${
              comparisonData.estimatedVsAverage < 0 ? 'text-green-600' : 'text-red-600'
            }`}>
              {comparisonData.estimatedVsAverage > 0 ? '+' : ''}{comparisonData.estimatedVsAverage}m
            </div>
            <div className="text-xs text-gray-500">
              {comparisonData.estimatedVsAverage < 0 
                ? (currentLanguage === 'zh' ? '比平均快' : 'faster')
                : (currentLanguage === 'zh' ? '比平均慢' : 'slower')
              }
            </div>
          </div>
        </div>

        {/* Sample Size */}
        <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
          <div>
            <div className="text-sm font-medium text-gray-900">
              {t('similarCases', 'Similar Cases')}
            </div>
            <div className="text-xs text-gray-600">
              {t('dataBasedOn', 'data based on')}
            </div>
          </div>
          <div className="text-right">
            <div className="text-lg font-semibold text-gray-900">
              {comparisonData.similarCasesCount.toLocaleString()}
            </div>
            <div className="text-xs text-gray-500">
              {t('cases', 'cases')}
            </div>
          </div>
        </div>
      </div>

      {/* Visual Progress Bar */}
      <div className="mt-4">
        <div className="flex items-center justify-between text-xs text-gray-600 mb-2">
          <span>{t('slower', 'Slower')}</span>
          <span>{t('average', 'Average')}</span>
          <span>{t('faster', 'Faster')}</span>
        </div>
        <div className="relative h-2 bg-gray-200 rounded-full">
          <div 
            className="absolute h-2 bg-gradient-to-r from-red-400 via-yellow-400 to-green-400 rounded-full"
            style={{ width: '100%' }}
          ></div>
          <div 
            className="absolute w-3 h-3 bg-white border-2 border-blue-500 rounded-full transform -translate-y-0.5"
            style={{ left: `${comparisonData.userPercentile}%`, transform: 'translateX(-50%) translateY(-2px)' }}
          ></div>
        </div>
      </div>

      {/* Additional Insights */}
      <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
        <div className="flex items-start">
          <span className="text-blue-500 mr-2">💡</span>
          <div className="text-sm text-blue-800">
            <div className="font-medium mb-1">
              {t('insight', 'Insight')}
            </div>
            <div>
              {currentLanguage === 'zh' 
                ? `基于您的案件类型和处理中心，您的进度比平均水平快${Math.abs(comparisonData.estimatedVsAverage)}个月。继续保持！`
                : `Based on your case type and processing center, you're ${Math.abs(comparisonData.estimatedVsAverage)} months ${comparisonData.estimatedVsAverage < 0 ? 'ahead of' : 'behind'} the average timeline. Keep it up!`
              }
            </div>
          </div>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="mt-4 text-xs text-gray-500 text-center">
        {currentLanguage === 'zh' 
          ? '* 基于匿名历史数据。个人结果可能有所不同。'
          : '* Based on anonymized historical data. Individual results may vary.'
        }
      </div>
    </div>
  );
}; 