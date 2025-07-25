import { NextRequest, NextResponse } from 'next/server';
import { UserCaseTracker, ApiResponse, CaseListResponse } from '@/types/tracking';
import { EstimationEngine } from '@/utils/estimationEngine';

// Shared data storage - in a real app, this would be a database
import { getCases, setCases, addCase, findCase } from '../shared-data';

let nextId = 1;

/**
 * GET /api/tracking/cases - Get all cases or user-specific cases
 */
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const userId = searchParams.get('user_id');
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '10');

    let filteredCases = getCases();
    
    if (userId) {
      filteredCases = cases.filter(c => c.user_id === userId);
    }

    // Pagination
    const startIndex = (page - 1) * limit;
    const endIndex = startIndex + limit;
    const paginatedCases = filteredCases.slice(startIndex, endIndex);

    const response: ApiResponse<CaseListResponse> = {
      success: true,
      data: {
        cases: paginatedCases,
        total: filteredCases.length,
        page,
        limit
      },
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(response);
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to fetch cases',
      timestamp: new Date().toISOString()
    }, { status: 500 });
  }
}

/**
 * POST /api/tracking/cases - Create a new case
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { user_id, visa_type, processing_center, priority_date, country_of_birth } = body;

    // Validate required fields
    if (!user_id || !visa_type || !processing_center || !priority_date || !country_of_birth) {
      return NextResponse.json({
        success: false,
        error: 'Missing required fields',
        timestamp: new Date().toISOString()
      }, { status: 400 });
    }

    // Check if user already has a case
    const existingCase = findCase(user_id);
    if (existingCase) {
      return NextResponse.json({
        success: false,
        error: 'User already has an active case',
        timestamp: new Date().toISOString()
      }, { status: 409 });
    }

    // Initialize new case
    const newCase = EstimationEngine.initializeCase(
      user_id,
      visa_type,
      processing_center,
      priority_date,
      country_of_birth
    );

    newCase.case_number = `MSC${String(nextId).padStart(10, '0')}`;
    addCase(newCase);
    nextId++;

    const response: ApiResponse<UserCaseTracker> = {
      success: true,
      data: newCase,
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(response, { status: 201 });
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to create case',
      timestamp: new Date().toISOString()
    }, { status: 500 });
  }
}

/**
 * PUT /api/tracking/cases/:id - Update a case
 */
export async function PUT(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const caseId = searchParams.get('id');
    const body = await request.json();

    if (!caseId) {
      return NextResponse.json({
        success: false,
        error: 'Case ID is required',
        timestamp: new Date().toISOString()
      }, { status: 400 });
    }

    const existingCase = findCase(caseId);
    if (!existingCase) {
      return NextResponse.json({
        success: false,
        error: 'Case not found',
        timestamp: new Date().toISOString()
      }, { status: 404 });
    }

    // Update case data
    const updatedCase = {
      ...existingCase,
      ...body,
      updated_at: new Date().toISOString()
    };

    const cases = getCases();
    const updatedCases = cases.map(c => c.user_id === caseId ? updatedCase : c);
    setCases(updatedCases);

    const response: ApiResponse<UserCaseTracker> = {
      success: true,
      data: updatedCase,
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(response);
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to update case',
      timestamp: new Date().toISOString()
    }, { status: 500 });
  }
} 