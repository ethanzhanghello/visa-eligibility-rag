import { sampleTrackingCases } from '../data/sampleTrackingData';

/**
 * Populate the API with sample tracking data for demo purposes
 */
export async function populateSampleData() {
  try {
    // Clear existing cases first (for demo)
    console.log('Populating sample tracking data...');

    for (const caseData of sampleTrackingCases) {
      try {
        const response = await fetch('/api/tracking/cases', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_id: caseData.user_id,
            visa_type: caseData.visa_type,
            processing_center: caseData.processing_center,
            priority_date: caseData.priority_date,
            country_of_birth: caseData.country_of_birth
          })
        });

        if (response.ok) {
          const result = await response.json();
          console.log(`Created case: ${result.data.case_number}`);

          // Update the case with the actual tracking data
          if (result.data.user_id) {
            const updateResponse = await fetch(`/api/tracking/cases?id=${result.data.user_id}`, {
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                ...caseData,
                case_number: result.data.case_number // Keep the generated case number
              })
            });

            if (updateResponse.ok) {
              console.log(`Updated case: ${result.data.case_number}`);
            }
          }
        } else {
          console.error(`Failed to create case for user ${caseData.user_id}`);
        }
      } catch (error) {
        console.error(`Error creating case for user ${caseData.user_id}:`, error);
      }
    }

    console.log('Sample data population completed');
    return true;
  } catch (error) {
    console.error('Failed to populate sample data:', error);
    return false;
  }
}

/**
 * Initialize sample data on app startup
 */
export function initializeSampleDataOnLoad() {
  // Only run in development mode
  if (typeof window !== 'undefined' && process.env.NODE_ENV === 'development') {
    // Wait a moment for the app to load
    setTimeout(() => {
      populateSampleData();
    }, 2000);
  }
} 