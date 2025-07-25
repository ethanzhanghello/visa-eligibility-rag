import { UserCaseTracker } from '@/types/tracking';

// Shared in-memory storage for demo purposes
// In a real application, this would be replaced with a database
let cases: UserCaseTracker[] = [];

export function getCases(): UserCaseTracker[] {
  return cases;
}

export function setCases(newCases: UserCaseTracker[]): void {
  cases = newCases;
}

export function addCase(newCase: UserCaseTracker): void {
  cases.push(newCase);
}

export function updateCase(userId: string, updates: Partial<UserCaseTracker>): boolean {
  const index = cases.findIndex(c => c.user_id === userId);
  if (index !== -1) {
    cases[index] = { ...cases[index], ...updates };
    return true;
  }
  return false;
}

export function findCase(userId: string): UserCaseTracker | undefined {
  return cases.find(c => c.user_id === userId);
} 