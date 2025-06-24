import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
from src.api.models import LowConfidenceQuestion, ReviewStatus
from src.api.question_tracker import QuestionTracker

logger = logging.getLogger(__name__)

class FAQIntegrationManager:
    def __init__(self, faq_file_path: str = "src/data/knowledge-base/faqs.json"):
        """
        Initialize FAQ integration manager.
        
        Args:
            faq_file_path: Path to the FAQ JSON file
        """
        self.faq_file_path = Path(faq_file_path)
        self.question_tracker = QuestionTracker()
        self._load_faq_data()
    
    def _load_faq_data(self):
        """Load existing FAQ data."""
        try:
            with open(self.faq_file_path, 'r', encoding='utf-8') as f:
                self.faq_data = json.load(f)
            logger.info(f"Loaded {len(self.faq_data.get('faqs', []))} existing FAQs")
        except FileNotFoundError:
            logger.warning("FAQ file not found, creating new structure")
            self.faq_data = {"faqs": []}
        except Exception as e:
            logger.error(f"Error loading FAQ data: {e}")
            self.faq_data = {"faqs": []}
    
    def _save_faq_data(self):
        """Save FAQ data to file."""
        try:
            with open(self.faq_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.faq_data, f, indent=2, ensure_ascii=False, default=str)
            logger.info("FAQ data saved successfully")
        except Exception as e:
            logger.error(f"Error saving FAQ data: {e}")
            raise
    
    def integrate_expert_review(self, question_id: str) -> bool:
        """
        Integrate an expert-reviewed question into the FAQ database.
        
        Args:
            question_id: ID of the question to integrate
            
        Returns:
            True if integration successful, False otherwise
        """
        question = self.question_tracker.get_question_by_id(question_id)
        if not question:
            logger.error(f"Question {question_id} not found")
            return False
        
        if question.status != ReviewStatus.APPROVED:
            logger.error(f"Question {question_id} is not approved for integration")
            return False
        
        if not question.expert_answer or not question.expert_sources:
            logger.error(f"Question {question_id} missing expert answer or sources")
            return False
        
        # Create new FAQ entry
        new_faq = {
            "id": f"expert_{question_id}",
            "question": question.question,
            "answer": question.expert_answer,
            "language": question.language,
            "category": "expert_reviewed",
            "sources": question.expert_sources,
            "expert_credentials": question.expert_credentials,
            "review_date": question.review_date.isoformat() if question.review_date else None,
            "confidence_score": question.confidence_score,
            "frequency_count": question.frequency_count,
            "audit_trail": question.audit_trail,
            "created_date": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        # Add to FAQ data
        self.faq_data["faqs"].append(new_faq)
        
        # Save updated FAQ data
        self._save_faq_data()
        
        # Update question status to integrated
        self.question_tracker.update_question_status(
            question_id, 
            ReviewStatus.APPROVED, 
            expert_reviewer=question.expert_reviewer
        )
        
        # Add integration to audit trail
        question.audit_trail.append({
            "action": "integrated_to_faq",
            "timestamp": datetime.now().isoformat(),
            "faq_id": new_faq["id"]
        })
        
        logger.info(f"Successfully integrated question {question_id} into FAQ database")
        return True
    
    def get_pending_integrations(self) -> List[Dict[str, Any]]:
        """Get list of approved questions pending integration into FAQ."""
        pending = []
        for question in self.question_tracker.questions.values():
            if (question.status == ReviewStatus.APPROVED and 
                question.expert_answer and 
                question.expert_sources):
                pending.append({
                    "id": question.id,
                    "question": question.question,
                    "language": question.language,
                    "expert_answer": question.expert_answer,
                    "expert_sources": question.expert_sources,
                    "expert_credentials": question.expert_credentials,
                    "frequency_count": question.frequency_count,
                    "review_date": question.review_date.isoformat() if question.review_date else None
                })
        
        return pending
    
    def validate_expert_review(self, question_id: str) -> Dict[str, Any]:
        """
        Validate an expert review for potential bias or issues.
        
        Args:
            question_id: ID of the question to validate
            
        Returns:
            Validation results
        """
        question = self.question_tracker.get_question_by_id(question_id)
        if not question:
            return {"valid": False, "errors": ["Question not found"]}
        
        validation_results = {
            "valid": True,
            "warnings": [],
            "errors": [],
            "suggestions": []
        }
        
        # Check for required fields
        if not question.expert_answer:
            validation_results["errors"].append("Missing expert answer")
            validation_results["valid"] = False
        
        if not question.expert_sources:
            validation_results["errors"].append("Missing expert sources")
            validation_results["valid"] = False
        
        if not question.expert_credentials:
            validation_results["warnings"].append("Missing expert credentials")
        
        # Check answer length
        if len(question.expert_answer) < 50:
            validation_results["warnings"].append("Expert answer seems too short")
        
        if len(question.expert_answer) > 2000:
            validation_results["warnings"].append("Expert answer seems too long")
        
        # Check for official sources
        official_sources = ["uscis.gov", "state.gov", "dhs.gov", "justice.gov", "immigration.gov"]
        has_official_source = any(
            any(official in source.lower() for official in official_sources)
            for source in question.expert_sources
        )
        
        if not has_official_source:
            validation_results["warnings"].append("No official government sources cited")
            validation_results["suggestions"].append("Consider adding official government sources")
        
        # Check for immigration-specific terms
        immigration_terms = ["visa", "green card", "immigration", "USCIS", "form", "petition"]
        has_immigration_terms = any(
            term.lower() in question.expert_answer.lower() 
            for term in immigration_terms
        )
        
        if not has_immigration_terms:
            validation_results["warnings"].append("Answer may not be immigration-related")
        
        # Check frequency
        if question.frequency_count < 2:
            validation_results["warnings"].append("Question asked only once - consider if it's common enough")
        
        return validation_results
    
    def get_integration_stats(self) -> Dict[str, Any]:
        """Get statistics about FAQ integration."""
        total_faqs = len(self.faq_data.get("faqs", []))
        expert_reviewed_faqs = len([
            faq for faq in self.faq_data.get("faqs", [])
            if faq.get("category") == "expert_reviewed"
        ])
        
        pending_integrations = len(self.get_pending_integrations())
        
        return {
            "total_faqs": total_faqs,
            "expert_reviewed_faqs": expert_reviewed_faqs,
            "pending_integrations": pending_integrations,
            "integration_rate": expert_reviewed_faqs / total_faqs if total_faqs > 0 else 0
        } 