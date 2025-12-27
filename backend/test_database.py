"""
Database Test Suite: CRUD Operations
Tests database models, relationships, and CRUD operations.
Run this to verify database functionality.
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.models.database import get_db, check_db_connection, engine
from app.models.ats_report import ATSReport, ATSReportCreate
from app.models.keyword import Keyword, KeywordType
from sqlalchemy.orm import Session
from datetime import datetime, timezone


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
    """Test creating a report with keywords"""
    print("\n📝 Testing report creation...")
    db = next(get_db())
    try:
        # Create a test report
        report = ATSReport(
            ats_score=85.5,
            skill_match_percentage=78.3,
            summary="Test report summary for database testing",
            resume_filename="test_resume.pdf",
            job_description="Test job description for database operations"
        )
        db.add(report)
        db.flush()
        
        # Add matched keywords
        matched_keywords = ["Python", "FastAPI", "PostgreSQL", "Docker"]
        for keyword_text in matched_keywords:
            keyword = Keyword(
                keyword=keyword_text,
                keyword_type=KeywordType.MATCHED,
                report_id=report.id,
                importance=0.8
            )
            db.add(keyword)
        
        # Add missing keywords
        missing_keywords = ["Kubernetes", "AWS", "CI/CD"]
        for keyword_text in missing_keywords:
            keyword = Keyword(
                keyword=keyword_text,
                keyword_type=KeywordType.MISSING,
                report_id=report.id,
                importance=0.6
            )
            db.add(keyword)
        
        db.commit()
        db.refresh(report)
        
        print(f"✅ Report created successfully! ID: {report.id}")
        print(f"   - Score: {report.ats_score}")
        print(f"   - Created at: {report.created_at}")
        return report.id
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating report: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        db.close()


def test_read_report(report_id: str):
    """Test reading a report with relationships"""
    print(f"\n📖 Testing report retrieval (ID: {report_id})...")
    db = next(get_db())
    try:
        report = db.query(ATSReport).filter(ATSReport.id == report_id).first()
        if not report:
            print("❌ Report not found!")
            return False
        
        # Test relationship loading
        keywords = db.query(Keyword).filter(Keyword.report_id == report_id).all()
        matched = [kw for kw in keywords if kw.keyword_type == KeywordType.MATCHED]
        missing = [kw for kw in keywords if kw.keyword_type == KeywordType.MISSING]
        
        print(f"✅ Report found!")
        print(f"   - Score: {report.ats_score}")
        print(f"   - Match: {report.skill_match_percentage}%")
        print(f"   - Matched keywords: {len(matched)}")
        print(f"   - Missing keywords: {len(missing)}")
        print(f"   - Total keywords: {len(keywords)}")
        
        # Verify relationship works
        assert len(keywords) > 0, "No keywords found"
        assert len(matched) > 0, "No matched keywords found"
        assert len(missing) > 0, "No missing keywords found"
        
        return True
    except Exception as e:
        print(f"❌ Error reading report: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_update_report(report_id: str):
    """Test updating a report"""
    print(f"\n✏️  Testing report update (ID: {report_id})...")
    db = next(get_db())
    try:
        report = db.query(ATSReport).filter(ATSReport.id == report_id).first()
        if not report:
            print("❌ Report not found!")
            return False
        
        # Update report
        original_score = report.ats_score
        report.ats_score = 90.0
        report.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(report)
        
        assert report.ats_score == 90.0, "Score not updated"
        assert report.updated_at is not None, "Updated timestamp not set"
        
        print(f"✅ Report updated successfully!")
        print(f"   - Old score: {original_score}")
        print(f"   - New score: {report.ats_score}")
        print(f"   - Updated at: {report.updated_at}")
        
        return True
    except Exception as e:
        db.rollback()
        print(f"❌ Error updating report: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_delete_keyword(report_id: str):
    """Test deleting a keyword (cascade should work)"""
    print(f"\n🗑️  Testing keyword deletion (Report ID: {report_id})...")
    db = next(get_db())
    try:
        keywords = db.query(Keyword).filter(Keyword.report_id == report_id).all()
        if not keywords:
            print("⚠️  No keywords to delete")
            return True
        
        keyword_to_delete = keywords[0]
        keyword_text = keyword_to_delete.keyword
        db.delete(keyword_to_delete)
        db.commit()
        
        # Verify deletion
        deleted = db.query(Keyword).filter(Keyword.id == keyword_to_delete.id).first()
        assert deleted is None, "Keyword not deleted"
        
        print(f"✅ Keyword '{keyword_text}' deleted successfully!")
        return True
    except Exception as e:
        db.rollback()
        print(f"❌ Error deleting keyword: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_delete_report(report_id: str):
    """Test deleting a report (should cascade delete keywords)"""
    print(f"\n🗑️  Testing report deletion with cascade (ID: {report_id})...")
    db = next(get_db())
    try:
        # Count keywords before deletion
        keywords_before = db.query(Keyword).filter(Keyword.report_id == report_id).count()
        
        report = db.query(ATSReport).filter(ATSReport.id == report_id).first()
        if not report:
            print("⚠️  Report not found (may have been deleted)")
            return True
        
        db.delete(report)
        db.commit()
        
        # Verify report deletion
        deleted_report = db.query(ATSReport).filter(ATSReport.id == report_id).first()
        assert deleted_report is None, "Report not deleted"
        
        # Verify cascade deletion of keywords
        keywords_after = db.query(Keyword).filter(Keyword.report_id == report_id).count()
        assert keywords_after == 0, f"Keywords not cascaded (found {keywords_after} remaining)"
        
        print(f"✅ Report deleted successfully!")
        print(f"   - {keywords_before} keywords were cascaded and deleted")
        return True
    except Exception as e:
        db.rollback()
        print(f"❌ Error deleting report: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_list_reports():
    """Test listing all reports"""
    print("\n📋 Testing report listing...")
    db = next(get_db())
    try:
        reports = db.query(ATSReport).order_by(ATSReport.created_at.desc()).all()
        print(f"✅ Found {len(reports)} report(s)")
        for report in reports[:5]:  # Show first 5
            keywords_count = db.query(Keyword).filter(Keyword.report_id == report.id).count()
            print(f"   - {report.id}: {report.ats_score}% ({keywords_count} keywords, created: {report.created_at})")
        return True
    except Exception as e:
        print(f"❌ Error listing reports: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_keyword_relationships():
    """Test keyword relationships and filtering"""
    print("\n🔗 Testing keyword relationships...")
    db = next(get_db())
    try:
        # Get all reports
        reports = db.query(ATSReport).limit(5).all()
        
        for report in reports:
            # Test relationship access
            keywords = db.query(Keyword).filter(Keyword.report_id == report.id).all()
            
            matched = [kw for kw in keywords if kw.keyword_type == KeywordType.MATCHED]
            missing = [kw for kw in keywords if kw.keyword_type == KeywordType.MISSING]
            
            print(f"   Report {report.id}:")
            print(f"     - Matched: {len(matched)} keywords")
            print(f"     - Missing: {len(missing)} keywords")
            
            # Verify enum values
            for kw in keywords:
                assert kw.keyword_type in [KeywordType.MATCHED, KeywordType.MISSING], \
                    f"Invalid keyword type: {kw.keyword_type}"
                assert kw.keyword_type.value in ["matched", "missing"], \
                    f"Invalid enum value: {kw.keyword_type.value}"
        
        print("✅ Keyword relationships test passed!")
        return True
    except Exception as e:
        print(f"❌ Error testing relationships: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()




def run_all_tests():
    """Run all database tests"""
    print("=" * 60)
    print("Database Test Suite: CRUD Operations")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test connection
    if test_connection():
        tests_passed += 1
    else:
        tests_failed += 1
        print("\n❌ Database connection failed. Please check your .env file and PostgreSQL.")
        return False
    
    # Test CRUD operations
    report_id = None
    try:
        report_id = test_create_report()
        if report_id:
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print(f"❌ Create report test failed: {e}\n")
        tests_failed += 1
    
    if report_id:
        try:
            if test_read_report(report_id):
                tests_passed += 1
            else:
                tests_failed += 1
        except Exception as e:
            print(f"❌ Read report test failed: {e}\n")
            tests_failed += 1
        
        try:
            if test_update_report(report_id):
                tests_passed += 1
            else:
                tests_failed += 1
        except Exception as e:
            print(f"❌ Update report test failed: {e}\n")
            tests_failed += 1
        
        try:
            if test_delete_keyword(report_id):
                tests_passed += 1
            else:
                tests_failed += 1
        except Exception as e:
            print(f"❌ Delete keyword test failed: {e}\n")
            tests_failed += 1
    
    try:
        if test_list_reports():
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print(f"❌ List reports test failed: {e}\n")
        tests_failed += 1
    
    try:
        if test_keyword_relationships():
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print(f"❌ Keyword relationships test failed: {e}\n")
        tests_failed += 1
    
    # Delete test report if it still exists
    if report_id:
        try:
            test_delete_report(report_id)
            tests_passed += 1
        except Exception as e:
            print(f"❌ Delete report test failed: {e}\n")
            tests_failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Test Results: {tests_passed} passed, {tests_failed} failed")
    print("=" * 60)
    
    if tests_failed == 0:
        print("\n🎉 All database tests passed!")
        return True
    else:
        print(f"\n⚠️  {tests_failed} test(s) failed. Please review the errors above.")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("ATS Resume Analyzer - Database Test Suite")
    print("=" * 60)
    
    try:
        run_all_tests()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ Database tests completed!")
    print("=" * 60)
