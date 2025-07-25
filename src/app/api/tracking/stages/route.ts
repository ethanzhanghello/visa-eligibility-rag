import { NextRequest, NextResponse } from 'next/server';
import { UserCaseTracker, ApiResponse, StageUpdateRequest, CaseUpdate } from '@/types/tracking';
import { EstimationEngine } from '@/utils/estimationEngine';

// Shared data storage - in a real app, this would be a database
// Import from a shared module to ensure consistency across routes
import { getCases, setCases } from '../shared-data';

let updates: CaseUpdate[] = [];

/**
 * POST /api/tracking/stages/complete - Mark a stage as complete
 */
export async function POST(request: NextRequest) {
  try {
    const body: StageUpdateRequest = await request.json();
    const { case_id, stage_id, completed, date_completed, notes } = body;

    // Validate required fields
    if (!case_id || stage_id === undefined || completed === undefined) {
      return NextResponse.json({
        success: false,
        error: 'Missing required fields: case_id, stage_id, completed',
        timestamp: new Date().toISOString()
      }, { status: 400 });
    }

    // Find the case
    const cases = getCases();
    const caseIndex = cases.findIndex(c => c.user_id === case_id);
    if (caseIndex === -1) {
      return NextResponse.json({
        success: false,
        error: 'Case not found',
        timestamp: new Date().toISOString()
      }, { status: 404 });
    }

    const caseData = cases[caseIndex];
    const engine = new EstimationEngine();

    if (completed) {
      // Mark stage as complete and recalculate estimates
      const completionDate = date_completed || new Date().toISOString().split('T')[0];
      const updates = engine.updateCaseEstimates(caseData, stage_id, completionDate);
      
      // Apply updates to the case
      const updatedCases = [...cases];
      updatedCases[caseIndex] = {
        ...caseData,
        ...updates
      };
      setCases(updatedCases);

      // Log the update
      const updateRecord: CaseUpdate = {
        case_id: case_id,
        stage_id: stage_id,
        action: 'complete',
        data: {
          date_completed: completionDate,
          notes: notes
        },
        admin_user_id: 'admin', // In real app, get from auth
        timestamp: new Date().toISOString()
      };
      updates.push(updateRecord);

    } else {
      // Update stage information without marking complete
      const stageIndex = caseData.tracker.findIndex(s => s.stage_id === stage_id);
      if (stageIndex !== -1) {
        caseData.tracker[stageIndex] = {
          ...caseData.tracker[stageIndex],
          notes: notes,
          updated_at: new Date().toISOString()
        };
        
        const updatedCases = [...cases];
        updatedCases[caseIndex] = {
          ...caseData,
          updated_at: new Date().toISOString()
        };
        setCases(updatedCases);
      }
    }

    const response: ApiResponse<UserCaseTracker> = {
      success: true,
      data: getCases()[caseIndex],
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(response);
  } catch (error) {
    console.error('Error updating stage:', error);
    return NextResponse.json({
      success: false,
      error: 'Failed to update stage',
      timestamp: new Date().toISOString()
    }, { status: 500 });
  }
}

/**
 * GET /api/tracking/stages/updates - Get recent stage updates
 */
export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const limit = parseInt(searchParams.get('limit') || '10');
    const case_id = searchParams.get('case_id');

    let filteredUpdates = updates;
    
    if (case_id) {
      filteredUpdates = updates.filter(u => u.case_id === case_id);
    }

    // Sort by timestamp (most recent first) and limit
    const recentUpdates = filteredUpdates
      .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
      .slice(0, limit);

    const response: ApiResponse<CaseUpdate[]> = {
      success: true,
      data: recentUpdates,
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(response);
  } catch (error) {
    return NextResponse.json({
      success: false,
      error: 'Failed to fetch updates',
      timestamp: new Date().toISOString()
    }, { status: 500 });
  }
} 