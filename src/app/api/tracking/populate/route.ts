import { NextRequest, NextResponse } from 'next/server';
import { ApiResponse } from '@/types/tracking';
import { setCases } from '../shared-data';
import { sampleTrackingCases } from '@/data/sampleTrackingData';

/**
 * POST /api/tracking/populate - Populate with sample data for demo
 */
export async function POST(request: NextRequest) {
  try {
    // Clear existing data and populate with sample cases
    setCases([...sampleTrackingCases]);

    const response: ApiResponse<{ message: string; count: number }> = {
      success: true,
      data: {
        message: 'Sample data populated successfully',
        count: sampleTrackingCases.length
      },
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(response);
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to populate sample data',
      timestamp: new Date().toISOString()
    }, { status: 500 });
  }
}

/**
 * GET /api/tracking/populate - Check if sample data is populated
 */
export async function GET(request: NextRequest) {
  try {
    const { getCases } = require('../shared-data');
    const cases = getCases();

    const response: ApiResponse<{ populated: boolean; count: number }> = {
      success: true,
      data: {
        populated: cases.length > 0,
        count: cases.length
      },
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(response);
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to check sample data status',
      timestamp: new Date().toISOString()
    }, { status: 500 });
  }
} 