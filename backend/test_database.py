"""
Test script to verify database connection and CRUD operations.
Run this after starting the server to test database functionality.
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.models.database import get_db, check_db_connection, engine
from app.models.ats_report import ATSReport
from app.models.keyword import Keyword, KeywordType
from sqlalchemy.orm import Session

def test_connection():
    """Test database connection"""
    print("🔌 Testing database connection...")
    if check_db_connection():
        print("✅ Database connection successful!")
        return True
    else:
        print("❌ Database connection failed!")
        return False

def test_create_report():
    """Test creating a report"""
    print("\n📝 Testing report creation...")
    db = next(get_db())
    try:
        # Create a test report
        report = ATSReport(
            ats_score=85.5,
            skill_match_percentage=78.3,
            summary="Test report summary",
            resume_filename="test_resume.pdf",
            job_description="Test job description"
        )
        db.add(report)
        db.flush()
        
        # Add keywords
        matched_keyword = Keyword(
            keyword="Python",
            keyword_type=KeywordType.MATCHED,
            report_id=report.id
        )
        missing_keyword = Keyword(
            keyword="Docker",
            keyword_type=KeywordType.MISSING,
            report_id=report.id
        )
        db.add(matched_keyword)
        db.add(missing_keyword)
        db.commit()
        
        print(f"✅ Report created successfully! ID: {report.id}")
        return report.id
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating report: {e}")
        return None
    finally:
        db.close()

def test_read_report(report_id: str):
    """Test reading a report"""
    print(f"\n📖 Testing report retrieval (ID: {report_id})...")
    db = next(get_db())
    try:
        report = db.query(ATSReport).filter(ATSReport.id == report_id).first()
        if report:
            keywords = db.query(Keyword).filter(Keyword.report_id == report_id).all()
            print(f"✅ Report found!")
            print(f"   - Score: {report.ats_score}")
            print(f"   - Match: {report.skill_match_percentage}%")
            print(f"   - Keywords: {len(keywords)}")
            return True
        else:
            print("❌ Report not found!")
            return False
    except Exception as e:
        print(f"❌ Error reading report: {e}")
        return False
    finally:
        db.close()

def test_list_reports():
    """Test listing reports"""
    print("\n📋 Testing report listing...")
    db = next(get_db())
    try:
        reports = db.query(ATSReport).all()
        print(f"✅ Found {len(reports)} report(s)")
        for report in reports:
            print(f"   - {report.id}: {report.ats_score}% (created: {report.created_at})")
        return True
    except Exception as e:
        print(f"❌ Error listing reports: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 50)
    print("ATS Resume Analyzer - Database Test Suite")
    print("=" * 50)
    
    # Test connection
    if not test_connection():
        print("\n❌ Database connection failed. Please check your .env file and PostgreSQL.")
        sys.exit(1)
    
    # Test CRUD operations
    report_id = test_create_report()
    if report_id:
        test_read_report(report_id)
    test_list_reports()
    
    print("\n" + "=" * 50)
    print("✅ Database tests completed!")
    print("=" * 50)

