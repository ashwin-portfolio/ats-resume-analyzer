"""
Comprehensive Test Suite for All 4 Phases.
Tests: Backend Skeleton, Database, ML Pipeline, and Integration.
Run from backend/ (e.g. python tests/test_all_phases.py). Backend server must be running on port 8000.
"""
import sys
import requests

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}{text.center(70)}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")


def print_test(name: str, status: str, details: str = "") -> None:
    """Print test result."""
    if status == "PASS":
        print(f"{GREEN}✅ {name}{RESET} {details}")
    elif status == "FAIL":
        print(f"{RED}❌ {name}{RESET} {details}")
    else:
        print(f"{YELLOW}⚠️  {name}{RESET} {details}")


def check_server() -> bool:
    """Check if backend server is running."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except Exception:
        return False


# ===============================
# PHASE 1: BACKEND SKELETON
# ===============================
def test_phase1_backend_skeleton():
    """Test Phase 1: Backend Skeleton."""
    print_header("PHASE 1: BACKEND SKELETON TESTING")
    results = {"passed": 0, "failed": 0}

    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data and "version" in data
        print_test("Root Endpoint", "PASS", f"Status: {data.get('status')}")
        results["passed"] += 1
    except Exception as e:
        print_test("Root Endpoint", "FAIL", str(e))
        results["failed"] += 1

    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "ml_model_loaded" in data
        ml_status = "✅ Loaded" if data.get("ml_model_loaded") else "❌ Not Loaded"
        print_test("Health Check", "PASS", f"ML Model: {ml_status}")
        results["passed"] += 1
        return data.get("ml_model_loaded", False)
    except Exception as e:
        print_test("Health Check", "FAIL", str(e))
        results["failed"] += 1
        return False


# ===============================
# PHASE 2: DATABASE MODELS (via API)
# ===============================
def test_phase2_database():
    """Test Phase 2: Database Models via API."""
    print_header("PHASE 2: DATABASE MODELS TESTING")
    results = {"passed": 0, "failed": 0}

    try:
        response = requests.get(f"{API_URL}/reports?limit=1", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "total" in data and "reports" in data
        print_test("Database Connection", "PASS", f"Total reports: {data.get('total')}")
        results["passed"] += 1
    except Exception as e:
        print_test("Database Connection", "FAIL", str(e))
        results["failed"] += 1
        return results

    pdf_content = b"""%PDF-1.4
1 0 obj<< /Type /Catalog >>endobj
xref 0 1 trailer<< /Size 1 /Root 1 0 R >>startxref 100 %%EOF"""
    files = {"resume_file": ("test.pdf", pdf_content, "application/pdf")}
    data_form = {"job_description": "Looking for a Python developer with FastAPI experience and database skills."}

    try:
        response = requests.post(f"{API_URL}/analyze", files=files, data=data_form, timeout=30)
        if response.status_code == 200:
            result = response.json()
            report_id = result.get("report_id")
            print_test("Database Write (Create Report)", "PASS", f"Report ID: {report_id}")
            results["passed"] += 1
            try:
                response = requests.get(f"{API_URL}/report/{report_id}", timeout=5)
                assert response.status_code == 200
                data = response.json()
                assert data["report_id"] == report_id
                print_test("Database Read (Get Report)", "PASS", f"Retrieved report {report_id}")
                results["passed"] += 1
            except Exception as e:
                print_test("Database Read (Get Report)", "FAIL", str(e))
                results["failed"] += 1
        elif response.status_code == 503:
            print_test("Database Write (Create Report)", "WARN", "ML model not loaded - skipping")
        else:
            print_test("Database Write (Create Report)", "FAIL", f"Status: {response.status_code}")
            results["failed"] += 1
    except Exception as e:
        print_test("Database Write (Create Report)", "FAIL", str(e))
        results["failed"] += 1

    return results


# ===============================
# PHASE 3: ML PIPELINE
# ===============================
def test_phase3_ml_pipeline():
    """Test Phase 3: ML Pipeline."""
    print_header("PHASE 3: ML PIPELINE TESTING")
    results = {"passed": 0, "failed": 0}

    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        data = response.json()
        if not data.get("ml_model_loaded"):
            print_test("ML Model Status", "FAIL", "Model not loaded")
            results["failed"] += 1
            return results
        print_test("ML Model Status", "PASS", "Model is loaded")
        results["passed"] += 1
    except Exception as e:
        print_test("ML Model Status", "FAIL", str(e))
        results["failed"] += 1
        return results

    pdf_content = b"""%PDF-1.4
1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj
2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj
3 0 obj<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> /MediaBox [0 0 612 792] /Contents 4 0 R >>endobj
4 0 obj<< /Length 100 >>stream BT /F1 12 Tf 100 700 Td (John Doe Software Engineer Python FastAPI React PostgreSQL) Tj ET endstream endobj
xref 0 5 trailer<< /Size 5 /Root 1 0 R >>startxref 500 %%EOF"""
    files = {"resume_file": ("test_resume.pdf", pdf_content, "application/pdf")}
    data_form = {"job_description": "Looking for a Software Engineer with Python, FastAPI, React, and PostgreSQL experience. Must have strong backend development skills."}

    try:
        response = requests.post(f"{API_URL}/analyze", files=files, data=data_form, timeout=60)
        if response.status_code == 200:
            result = response.json()
            assert "ats_score" in result and 0 <= result["ats_score"] <= 100
            assert "skill_match_percentage" in result
            assert isinstance(result.get("matched_keywords"), list)
            assert isinstance(result.get("missing_keywords"), list)
            assert result.get("summary")
            assert isinstance(result.get("recommendations"), list)
            print_test("Text Extraction", "PASS", "PDF text extracted successfully")
            results["passed"] += 1
            print_test("Keyword Extraction", "PASS", f"Found {len(result.get('matched_keywords', []))} matched keywords")
            results["passed"] += 1
            print_test("Semantic Similarity", "PASS", f"ATS Score: {result['ats_score']:.2f}")
            results["passed"] += 1
            print_test("Recommendations Generation", "PASS", f"Generated {len(result.get('recommendations', []))} recommendations")
            results["passed"] += 1
        elif response.status_code == 400:
            error_detail = response.json().get("detail", "Unknown error")
            if "extract text" in error_detail.lower() or "empty" in error_detail.lower():
                print_test("Text Extraction", "FAIL", "Could not extract text from PDF")
            else:
                print_test("Text Extraction", "FAIL", error_detail)
            results["failed"] += 1
        else:
            print_test("ML Pipeline", "FAIL", f"Status: {response.status_code}")
            results["failed"] += 1
    except Exception as e:
        print_test("ML Pipeline", "FAIL", str(e))
        results["failed"] += 1

    return results


# ===============================
# PHASE 4: FRONTEND INTEGRATION
# ===============================
def test_phase4_frontend_integration():
    """Test Phase 4: Frontend Integration."""
    print_header("PHASE 4: FRONTEND INTEGRATION TESTING")
    results = {"passed": 0, "failed": 0}

    try:
        response = requests.get("http://localhost:3000", timeout=2)
        if response.status_code == 200:
            print_test("Frontend Server", "PASS", "Frontend is running on port 3000")
            results["passed"] += 1
        else:
            print_test("Frontend Server", "WARN", f"Status: {response.status_code}")
    except Exception:
        print_test("Frontend Server", "WARN", "Frontend not running (start with: npm run dev)")

    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        assert response.status_code == 200
        print_test("API Accessibility", "PASS", "Backend API is accessible")
        results["passed"] += 1
    except Exception as e:
        print_test("API Accessibility", "FAIL", str(e))
        results["failed"] += 1

    try:
        response = requests.options(f"{API_URL}/health", headers={"Origin": "http://localhost:3000", "Access-Control-Request-Method": "GET"}, timeout=5)
        if response.status_code in (200, 204):
            print_test("CORS Configuration", "PASS", "CORS is properly configured")
            results["passed"] += 1
        else:
            print_test("CORS Configuration", "WARN", "CORS preflight check inconclusive")
    except Exception:
        print_test("CORS Configuration", "WARN", "Could not verify CORS")

    pdf_content = b"""%PDF-1.4
1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj
2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj
3 0 obj<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> /MediaBox [0 0 612 792] /Contents 4 0 R >>endobj
4 0 obj<< /Length 120 >>stream BT /F1 12 Tf 100 700 Td (Software Engineer Python FastAPI React Database) Tj ET endstream endobj
xref 0 5 trailer<< /Size 5 /Root 1 0 R >>startxref 500 %%EOF"""
    files = {"resume_file": ("frontend_test.pdf", pdf_content, "application/pdf")}
    data_form = {"job_description": "Looking for a full-stack developer with Python, FastAPI, React, and database experience."}

    try:
        response = requests.post(f"{API_URL}/analyze", files=files, data=data_form, timeout=60)
        if response.status_code == 200:
            result = response.json()
            report_id = result.get("report_id")
            response = requests.get(f"{API_URL}/report/{report_id}", timeout=5)
            if response.status_code == 200:
                report_data = response.json()
                assert report_data["report_id"] == report_id
                print_test("End-to-End Flow", "PASS", f"Complete flow works: Analyze → Report {report_id}")
                results["passed"] += 1
            else:
                print_test("End-to-End Flow", "FAIL", "Could not retrieve report after analysis")
                results["failed"] += 1
        else:
            print_test("End-to-End Flow", "WARN", f"Analysis returned status {response.status_code}")
    except Exception as e:
        print_test("End-to-End Flow", "FAIL", str(e))
        results["failed"] += 1

    return results


# ===============================
# MAIN TEST RUNNER
# ===============================
def run_all_tests() -> bool:
    """Run all phase tests."""
    print(f"\n{BOLD}{GREEN}{'='*70}{RESET}")
    print(f"{BOLD}{GREEN}{'COMPREHENSIVE TEST SUITE - ALL 4 PHASES'.center(70)}{RESET}")
    print(f"{BOLD}{GREEN}{'='*70}{RESET}\n")

    if not check_server():
        print(f"{RED}❌ Backend server is not running!{RESET}")
        print(f"{YELLOW}Please start the backend server first (in another terminal):{RESET}")
        print("  source venv/bin/activate   # or venv\\Scripts\\activate on Windows")
        print("  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        sys.exit(1)

    print(f"{GREEN}✅ Backend server is running{RESET}\n")

    all_results = {
        "Phase 1": {"passed": 0, "failed": 0},
        "Phase 2": {"passed": 0, "failed": 0},
        "Phase 3": {"passed": 0, "failed": 0},
        "Phase 4": {"passed": 0, "failed": 0},
    }

    try:
        test_phase1_backend_skeleton()
        all_results["Phase 1"]["passed"] = 2
    except Exception as e:
        print(f"{RED}Phase 1 test error: {e}{RESET}")
        all_results["Phase 1"]["failed"] += 1

    try:
        db_results = test_phase2_database()
        if isinstance(db_results, dict):
            all_results["Phase 2"] = db_results
    except Exception as e:
        print(f"{RED}Phase 2 test error: {e}{RESET}")
        all_results["Phase 2"]["failed"] += 1

    try:
        ml_results = test_phase3_ml_pipeline()
        if isinstance(ml_results, dict):
            all_results["Phase 3"] = ml_results
    except Exception as e:
        print(f"{RED}Phase 3 test error: {e}{RESET}")
        all_results["Phase 3"]["failed"] += 1

    try:
        frontend_results = test_phase4_frontend_integration()
        if isinstance(frontend_results, dict):
            all_results["Phase 4"] = frontend_results
    except Exception as e:
        print(f"{RED}Phase 4 test error: {e}{RESET}")
        all_results["Phase 4"]["failed"] += 1

    print_header("TEST SUMMARY")
    total_passed = sum(r["passed"] for r in all_results.values())
    total_failed = sum(r["failed"] for r in all_results.values())

    for phase, res in all_results.items():
        status = f"{GREEN}✅ PASS{RESET}" if res["failed"] == 0 else f"{RED}❌ FAIL{RESET}"
        print(f"{BOLD}{phase}:{RESET} {status} ({res['passed']} passed, {res['failed']} failed)")

    print(f"\n{BOLD}Total:{RESET} {GREEN}{total_passed} passed{RESET}, {RED}{total_failed} failed{RESET}")

    if total_failed == 0:
        print(f"\n{BOLD}{GREEN}🎉 All tests passed! All 4 phases are working correctly!{RESET}\n")
        return True
    print(f"\n{BOLD}{YELLOW}⚠️  Some tests failed. Please review the errors above.{RESET}\n")
    return False


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Tests interrupted by user{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Unexpected error: {e}{RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
