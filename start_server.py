#!/usr/bin/env python3
"""
Startup script for the Green Card RAG Helper API.
Validates configuration and provides helpful error messages.
"""
import os
import sys
import logging
from pathlib import Path

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config import config

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, config.logging.level),
        format=config.logging.format,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(config.logging.file) if config.logging.file else logging.NullHandler()
        ]
    )

def validate_environment():
    """Validate environment and provide helpful messages."""
    print("🌍 Green Card RAG Helper - Configuration Validation")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Validate configuration
    print("\n🔧 Validating configuration...")
    errors = config.validate()
    
    if errors:
        print("❌ Configuration validation failed:")
        for error in errors:
            print(f"   - {error}")
        
        print("\n💡 To fix these issues:")
        print("   1. Set the OPENAI_API_KEY environment variable:")
        print("      export OPENAI_API_KEY='your-api-key-here'")
        print("   2. Check other environment variables in src/config.py")
        print("   3. Ensure all required directories exist")
        return False
    
    print("✅ Configuration validation passed")
    
    # Check database directory
    db_path = Path(config.get_database_path())
    if not db_path.exists():
        print(f"📁 Creating database directory: {db_path}")
        db_path.mkdir(parents=True, exist_ok=True)
    else:
        print(f"✅ Database directory exists: {db_path}")
    
    # Check data files
    faq_path = Path("src/data/knowledge-base/faqs.json")
    if not faq_path.exists():
        print("❌ FAQ data file not found. Please ensure src/data/knowledge-base/faqs.json exists")
        return False
    else:
        print(f"✅ FAQ data file found: {faq_path}")
    
    # Check if database is populated
    try:
        from src.vector_db.vector_db_manager import VectorDBManager
        db_manager = VectorDBManager()
        stats = db_manager.get_collection_stats()
        
        if stats["is_empty"]:
            print("⚠️  Database is empty. Run 'python populate_db.py' to populate it")
        else:
            print(f"✅ Database has {stats['document_count']} documents")
    except Exception as e:
        print(f"⚠️  Could not check database status: {e}")
    
    return True

def print_startup_info():
    """Print startup information."""
    print("\n🚀 Starting Green Card RAG Helper API...")
    print(f"   Host: {config.api.host}")
    print(f"   Port: {config.api.port}")
    print(f"   Model: {config.llm.model_name}")
    print(f"   Confidence Threshold: {config.confidence.threshold}")
    print(f"   Rate Limiting: {'Enabled' if config.security.enable_rate_limiting else 'Disabled'}")
    
    if config.llm.api_key:
        print("   API Key: ✅ Set")
    else:
        print("   API Key: ❌ Not set (using mock LLM)")
    
    print("\n📚 Available endpoints:")
    print("   - POST /query - Submit immigration questions")
    print("   - GET /health - Check API health")
    print("   - GET /config - View configuration")
    print("   - GET /system/info - System information")
    print("   - GET /docs - API documentation")
    
    print("\n🔗 API will be available at:")
    print(f"   http://{config.api.host}:{config.api.port}")
    print(f"   Documentation: http://{config.api.host}:{config.api.port}/docs")

def main():
    """Main startup function."""
    try:
        # Setup logging
        setup_logging()
        
        # Validate environment
        if not validate_environment():
            print("\n❌ Startup validation failed. Please fix the issues above.")
            sys.exit(1)
        
        # Print startup info
        print_startup_info()
        
        # Start the server
        print("\n" + "=" * 50)
        import uvicorn
        uvicorn.run(
            "src.api.main:app",
            host=config.api.host,
            port=config.api.port,
            reload=config.api.reload,
            workers=config.api.workers
        )
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to start server: {e}")
        logging.exception("Startup error")
        sys.exit(1)

if __name__ == "__main__":
    main() 