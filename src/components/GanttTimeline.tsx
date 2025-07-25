import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { TimelineStep } from '../types';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface GanttTimelineProps {
  steps: TimelineStep[];
  currentLanguage: string;
}

interface GanttDataPoint {
  name: string;
  startDate: number;
  duration: number;
  endDate: number;
  status: string;
  color: string;
}

export const GanttTimeline: React.FC<GanttTimelineProps> = ({
  steps,
  currentLanguage
}) => {
  const { t } = useTranslation();
  const [viewType, setViewType] = useState<'weeks' | 'months'>('months');

  // Calculate Gantt chart data
  const calculateGanttData = (): GanttDataPoint[] => {
    const baseDate = new Date('2024-03-01'); // Starting point
    let currentDate = new Date(baseDate);
    
    return steps.map((step, index) => {
      const stepName = currentLanguage === 'zh' ? step.zh.title : step.en.title;
      const shortName = stepName.length > 20 ? stepName.substring(0, 17) + '...' : stepName;
      
      const startTime = currentDate.getTime();
      const duration = step.processingTime ? step.processingTime.average : 30; // days
      
      const endDate = new Date(currentDate);
      endDate.setDate(endDate.getDate() + duration);
      
      const color = getStatusColor(step.status);
      
      currentDate = new Date(endDate); // Next step starts when this one ends
      
      return {
        name: shortName,
        startDate: viewType === 'weeks' 
          ? Math.floor((startTime - baseDate.getTime()) / (1000 * 60 * 60 * 24 * 7))
          : Math.floor((startTime - baseDate.getTime()) / (1000 * 60 * 60 * 24 * 30)),
        duration: viewType === 'weeks' 
          ? Math.ceil(duration / 7)
          : Math.ceil(duration / 30),
        endDate: viewType === 'weeks'
          ? Math.floor((endDate.getTime() - baseDate.getTime()) / (1000 * 60 * 60 * 24 * 7))
          : Math.floor((endDate.getTime() - baseDate.getTime()) / (1000 * 60 * 60 * 24 * 30)),
        status: step.status,
        color
      };
    });
  };

  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'completed': return '#10B981'; // Green
      case 'in_progress': return '#3B82F6'; // Blue
      case 'pending': return '#F59E0B'; // Yellow
      default: return '#6B7280'; // Gray
    }
  };

  const ganttData = calculateGanttData();
  const maxDuration = Math.max(...ganttData.map(d => d.endDate)) + 2;

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-900">{data.name}</p>
          <p className="text-sm text-gray-600">
            {t('duration', 'Duration')}: {data.duration} {viewType === 'weeks' ? t('weeks', 'weeks') : t('months', 'months')}
          </p>
          <p className="text-sm text-gray-600">
            {t('status', 'Status')}: {t(data.status, data.status)}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900">
          📊 {t('ganttTimeline', 'Timeline Chart')}
        </h2>
        <div className="flex space-x-2">
          <button
            onClick={() => setViewType('weeks')}
            className={`px-3 py-1 text-sm rounded ${
              viewType === 'weeks' 
                ? 'bg-blue-100 text-blue-800' 
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {t('weeks', 'Weeks')}
          </button>
          <button
            onClick={() => setViewType('months')}
            className={`px-3 py-1 text-sm rounded ${
              viewType === 'months' 
                ? 'bg-blue-100 text-blue-800' 
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {t('months', 'Months')}
          </button>
        </div>
      </div>

      <div className="h-96 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            layout="horizontal"
            data={ganttData}
            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              type="number" 
              domain={[0, maxDuration]}
              tickFormatter={(value) => `${value} ${viewType === 'weeks' ? 'W' : 'M'}`}
            />
            <YAxis 
              type="category" 
              dataKey="name" 
              width={150}
              tick={{ fontSize: 12 }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar 
              dataKey="duration" 
              fill="#3B82F6"
              radius={[0, 4, 4, 0]}
            >
              {ganttData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Legend */}
      <div className="flex items-center justify-center space-x-6 mt-4 text-sm">
        <div className="flex items-center">
          <div className="w-3 h-3 bg-green-500 rounded mr-2"></div>
          <span>{t('completed', 'Completed')}</span>
        </div>
        <div className="flex items-center">
          <div className="w-3 h-3 bg-blue-500 rounded mr-2"></div>
          <span>{t('inProgress', 'In Progress')}</span>
        </div>
        <div className="flex items-center">
          <div className="w-3 h-3 bg-yellow-500 rounded mr-2"></div>
          <span>{t('pending', 'Pending')}</span>
        </div>
        <div className="flex items-center">
          <div className="w-3 h-3 bg-gray-500 rounded mr-2"></div>
          <span>{t('estimated', 'Estimated')}</span>
        </div>
      </div>

      {/* Summary */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h4 className="font-medium text-gray-900 mb-2">
          📈 {t('timelineInsights', 'Timeline Insights')}
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <span className="text-gray-600">{t('totalDuration', 'Total Duration')}:</span>
            <span className="ml-2 font-medium">
              {Math.ceil(ganttData.reduce((sum, step) => sum + step.duration, 0))} {viewType === 'weeks' ? t('weeks', 'weeks') : t('months', 'months')}
            </span>
          </div>
          <div>
            <span className="text-gray-600">{t('completedSteps', 'Completed')}:</span>
            <span className="ml-2 font-medium">
              {steps.filter(s => s.status === 'completed').length}/{steps.length}
            </span>
          </div>
          <div>
            <span className="text-gray-600">{t('estimatedCompletion', 'Est. Completion')}:</span>
            <span className="ml-2 font-medium">
              {new Date(Date.now() + ganttData.reduce((sum, step) => sum + step.duration, 0) * (viewType === 'weeks' ? 7 : 30) * 24 * 60 * 60 * 1000).toLocaleDateString()}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}; 