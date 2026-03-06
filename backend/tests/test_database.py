"""
Database Test Suite: CRUD Operations.
Tests database models, relationships, and CRUD. Requires database configured in .env.
Run from backend/ (e.g. python tests/test_database.py).
"""
import sys
from pathlib import Path

# Add backend (parent of tests/) to path so "app" imports resolve
_backend = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_backend))

from app.models.database import get_db, check_db_connection
from app.models.ats_report import ATSReport
from app.models.keyword import Keyword, KeywordType
from datetime import datetime, timezone


def test_connection() -> bool:
    """Test database connection."""
    print("🔌 Testing database connection...")
    if check_db_connection():
        print("✅ Database connection successful!")
        return True
    print("❌ Database connection failed!")
    return False


def test_create_report():
    """Test creating a report with keywords. Returns report_id or None."""
    print("\n📝 Testing report creation...")
    db = next(get_db())
    try:
        report = ATSReport(
            ats_score=85.5,
            skill_match_percentage=78.3,
            summary="Test report summary for database testing",
            resume_filename="test_resume.pdf",
            job_description="Test job description for database operations",
        )
        db.add(report)
        db.flush()

        for keyword_text in ["Python", "FastAPI", "PostgreSQL", "Docker"]:
            db.add(Keyword(keyword=keyword_text, keyword_type=KeywordType.MATCHED, report_id=report.id, importance=0.8))
        for keyword_text in ["Kubernetes", "AWS", "CI/CD"]:
            db.add(Keyword(keyword=keyword_text, keyword_type=KeywordType.MISSING, report_id=report.id, importance=0.6))

        db.commit()
        db.refresh(report)
        print(f"✅ Report created successfully! ID: {report.id}")
        print(f"   - Score: {report.ats_score}, Created at: {report.created_at}")
        return report.id
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating report: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        db.close()


def test_read_report(report_id: str) -> bool:
    """Test reading a report with relationships."""
    print(f"\n📖 Testing report retrieval (ID: {report_id})...")
    db = next(get_db())
    try:
        report = db.query(ATSReport).filter(ATSReport.id == report_id).first()
        if not report:
            print("❌ Report not found!")
            return False

        keywords = db.query(Keyword).filter(Keyword.report_id == report_id).all()
        matched = [kw for kw in keywords if kw.keyword_type == KeywordType.MATCHED]
        missing = [kw for kw in keywords if kw.keyword_type == KeywordType.MISSING]

        print(f"✅ Report found! Score: {report.ats_score}, Match: {report.skill_match_percentage}%")
        print(f"   - Matched: {len(matched)}, Missing: {len(missing)}")

        assert len(keywords) > 0 and len(matched) > 0 and len(missing) > 0
        return True
    except Exception as e:
        print(f"❌ Error reading report: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_update_report(report_id: str) -> bool:
    """Test updating a report."""
    print(f"\n✏️  Testing report update (ID: {report_id})...")
    db = next(get_db())
    try:
        report = db.query(ATSReport).filter(ATSReport.id == report_id).first()
        if not report:
            print("❌ Report not found!")
            return False

        report.ats_score = 90.0
        report.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(report)

        assert report.ats_score == 90.0 and report.updated_at is not None
        print(f"✅ Report updated successfully! New score: {report.ats_score}")
        return True
    except Exception as e:
        db.rollback()
        print(f"❌ Error updating report: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_delete_keyword(report_id: str) -> bool:
    """Test deleting a keyword."""
    print(f"\n🗑️  Testing keyword deletion (Report ID: {report_id})...")
    db = next(get_db())
    try:
        keywords = db.query(Keyword).filter(Keyword.report_id == report_id).all()
        if not keywords:
            print("⚠️  No keywords to delete")
            return True

        kw = keywords[0]
        db.delete(kw)
        db.commit()
        deleted = db.query(Keyword).filter(Keyword.id == kw.id).first()
        assert deleted is None
        print(f"✅ Keyword '{kw.keyword}' deleted successfully!")
        return True
    except Exception as e:
        db.rollback()
        print(f"❌ Error deleting keyword: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_delete_report(report_id: str) -> bool:
    """Test deleting a report (cascade delete keywords)."""
    print(f"\n🗑️  Testing report deletion with cascade (ID: {report_id})...")
    db = next(get_db())
    try:
        keywords_before = db.query(Keyword).filter(Keyword.report_id == report_id).count()
        report = db.query(ATSReport).filter(ATSReport.id == report_id).first()
        if not report:
            print("⚠️  Report not found (may have been deleted)")
            return True

        db.delete(report)
        db.commit()

        assert db.query(ATSReport).filter(ATSReport.id == report_id).first() is None
        assert db.query(Keyword).filter(Keyword.report_id == report_id).count() == 0
        print(f"✅ Report deleted successfully! {keywords_before} keywords cascaded.")
        return True
    except Exception as e:
        db.rollback()
        print(f"❌ Error deleting report: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_list_reports() -> bool:
    """Test listing all reports."""
    print("\n📋 Testing report listing...")
    db = next(get_db())
    try:
        reports = db.query(ATSReport).order_by(ATSReport.created_at.desc()).all()
        print(f"✅ Found {len(reports)} report(s)")
        for report in reports[:5]:
            count = db.query(Keyword).filter(Keyword.report_id == report.id).count()
            print(f"   - {report.id}: {report.ats_score}% ({count} keywords)")
        return True
    except Exception as e:
        print(f"❌ Error listing reports: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_keyword_relationships() -> bool:
    """Test keyword relationships and filtering."""
    print("\n🔗 Testing keyword relationships...")
    db = next(get_db())
    try:
        for report in db.query(ATSReport).limit(5).all():
            keywords = db.query(Keyword).filter(Keyword.report_id == report.id).all()
            matched = [kw for kw in keywords if kw.keyword_type == KeywordType.MATCHED]
            missing = [kw for kw in keywords if kw.keyword_type == KeywordType.MISSING]
            print(f"   Report {report.id}: Matched {len(matched)}, Missing {len(missing)}")
            for kw in keywords:
                assert kw.keyword_type in (KeywordType.MATCHED, KeywordType.MISSING)
                assert kw.keyword_type.value in ("matched", "missing")
        print("✅ Keyword relationships test passed!")
        return True
    except Exception as e:
        print(f"❌ Error testing relationships: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def run_all_tests() -> bool:
    """Run all database tests."""
    print("=" * 60)
    print("Database Test Suite: CRUD Operations")
    print("=" * 60)

    tests_passed = 0
    tests_failed = 0

    if not test_connection():
        tests_failed += 1
        print("\n❌ Database connection failed. Check .env and PostgreSQL.")
        return False
    tests_passed += 1

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
        for fn in (test_read_report, test_update_report, test_delete_keyword):
            try:
                if fn(report_id):
                    tests_passed += 1
                else:
                    tests_failed += 1
            except Exception as e:
                print(f"❌ {fn.__name__} failed: {e}\n")
                tests_failed += 1

    for fn in (test_list_reports, test_keyword_relationships):
        try:
            if fn():
                tests_passed += 1
            else:
                tests_failed += 1
        except Exception as e:
            print(f"❌ {fn.__name__} failed: {e}\n")
            tests_failed += 1

    if report_id:
        try:
            if test_delete_report(report_id):
                tests_passed += 1
            else:
                tests_failed += 1
        except Exception as e:
            print(f"❌ test_delete_report failed: {e}\n")
            tests_failed += 1

    print("\n" + "=" * 60)
    print(f"Test Results: {tests_passed} passed, {tests_failed} failed")
    print("=" * 60)

    if tests_failed == 0:
        print("\n🎉 All database tests passed!")
        return True
    print(f"\n⚠️  {tests_failed} test(s) failed. Please review the errors above.")
    return False


if __name__ == "__main__":
    print("=" * 60)
    print("ATS Resume Analyzer - Database Test Suite")
    print("=" * 60)

    try:
        success = run_all_tests()
        print("\n✅ Database tests completed!" if success else "\n⚠️  Some tests failed.")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
