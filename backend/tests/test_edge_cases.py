"""
Edge Case Testing Suite.
Tests file upload, job description, and network edge cases.
Run from backend/ (e.g. python tests/test_edge_cases.py). Backend server must be running on port 8000.
"""
import sys
import requests

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header(text: str) -> None:
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}{text.center(70)}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")


def print_test(name: str, status: str, details: str = "") -> None:
    if status == "PASS":
        print(f"{GREEN}✅ {name}{RESET} {details}")
    elif status == "FAIL":
        print(f"{RED}❌ {name}{RESET} {details}")
    else:
        print(f"{YELLOW}⚠️  {name}{RESET} {details}")


def test_file_upload_edge_cases():
    """Test file upload edge cases."""
    print_header("FILE UPLOAD EDGE CASES")
    results = {"passed": 0, "failed": 0}

    try:
        files = {"resume_file": ("empty.pdf", b"", "application/pdf")}
        data = {"job_description": "Test job description with enough characters"}
        response = requests.post(f"{API_URL}/analyze", files=files, data=data, timeout=10)
        assert response.status_code == 400
        print_test("Empty File", "PASS", "Correctly rejected empty file")
        results["passed"] += 1
    except Exception as e:
        print_test("Empty File", "FAIL", str(e))
        results["failed"] += 1

    try:
        large_content = b"x" * (11 * 1024 * 1024)
        files = {"resume_file": ("large.pdf", large_content, "application/pdf")}
        data = {"job_description": "Test job description with enough characters"}
        response = requests.post(f"{API_URL}/analyze", files=files, data=data, timeout=10)
        assert response.status_code == 413
        print_test("Large File (>10MB)", "PASS", "Correctly rejected oversized file")
        results["passed"] += 1
    except Exception as e:
        print_test("Large File (>10MB)", "FAIL", str(e))
        results["failed"] += 1

    try:
        files = {"resume_file": ("test.txt", b"This is a text file", "text/plain")}
        data = {"job_description": "Test job description with enough characters"}
        response = requests.post(f"{API_URL}/analyze", files=files, data=data, timeout=10)
        assert response.status_code == 400
        print_test("Invalid File Type", "PASS", "Correctly rejected invalid file type")
        results["passed"] += 1
    except Exception as e:
        print_test("Invalid File Type", "FAIL", str(e))
        results["failed"] += 1

    try:
        files = {"resume_file": ("noextension", b"pdf content", "application/pdf")}
        data = {"job_description": "Test job description with enough characters"}
        response = requests.post(f"{API_URL}/analyze", files=files, data=data, timeout=10)
        assert response.status_code == 400
        print_test("File Without Extension", "PASS", "Correctly rejected file without extension")
        results["passed"] += 1
    except Exception as e:
        print_test("File Without Extension", "FAIL", str(e))
        results["failed"] += 1

    try:
        pdf_content = b"%PDF-1.4 minimal pdf"
        files = {"resume_file": ("file with spaces & special chars!.pdf", pdf_content, "application/pdf")}
        data = {"job_description": "Test job description with enough characters to pass validation"}
        response = requests.post(f"{API_URL}/analyze", files=files, data=data, timeout=30)
        assert response.status_code in (200, 400, 503)
        print_test("Special Characters in Filename", "PASS", f"Handled gracefully (status: {response.status_code})")
        results["passed"] += 1
    except Exception as e:
        print_test("Special Characters in Filename", "FAIL", str(e))
        results["failed"] += 1

    return results


def test_job_description_edge_cases():
    """Test job description edge cases."""
    print_header("JOB DESCRIPTION EDGE CASES")
    results = {"passed": 0, "failed": 0}
    pdf_content = b"%PDF-1.4 minimal pdf"

    try:
        files = {"resume_file": ("test.pdf", pdf_content, "application/pdf")}
        data = {"job_description": ""}
        response = requests.post(f"{API_URL}/analyze", files=files, data=data, timeout=10)
        assert response.status_code == 400
        print_test("Empty Job Description", "PASS", "Correctly rejected empty description")
        results["passed"] += 1
    except Exception as e:
        print_test("Empty Job Description", "FAIL", str(e))
        results["failed"] += 1

    try:
        files = {"resume_file": ("test.pdf", pdf_content, "application/pdf")}
        data = {"job_description": "Short"}
        response = requests.post(f"{API_URL}/analyze", files=files, data=data, timeout=10)
        assert response.status_code == 400
        print_test("Short Job Description", "PASS", "Correctly rejected short description")
        results["passed"] += 1
    except Exception as e:
        print_test("Short Job Description", "FAIL", str(e))
        results["failed"] += 1

    try:
        files = {"resume_file": ("test.pdf", pdf_content, "application/pdf")}
        data = {"job_description": "   \n\t   "}
        response = requests.post(f"{API_URL}/analyze", files=files, data=data, timeout=10)
        assert response.status_code == 400
        print_test("Whitespace Only", "PASS", "Correctly rejected whitespace-only description")
        results["passed"] += 1
    except Exception as e:
        print_test("Whitespace Only", "FAIL", str(e))
        results["failed"] += 1

    try:
        files = {"resume_file": ("test.pdf", pdf_content, "application/pdf")}
        data = {"job_description": "A" * 50000}
        response = requests.post(f"{API_URL}/analyze", files=files, data=data, timeout=60)
        assert response.status_code in (200, 400, 413, 503)
        print_test("Very Long Job Description", "PASS", f"Handled gracefully (status: {response.status_code})")
        results["passed"] += 1
    except Exception as e:
        print_test("Very Long Job Description", "FAIL", str(e))
        results["failed"] += 1

    return results


def test_network_edge_cases():
    """Test network-related edge cases."""
    print_header("NETWORK EDGE CASES")
    results = {"passed": 0, "failed": 0}

    try:
        response = requests.get(f"{API_URL}/report/invalid_id_12345", timeout=5)
        assert response.status_code == 404
        print_test("Invalid Report ID", "PASS", "Correctly returned 404")
        results["passed"] += 1
    except Exception as e:
        print_test("Invalid Report ID", "FAIL", str(e))
        results["failed"] += 1

    try:
        response = requests.get(f"{API_URL}/report/../../etc/passwd", timeout=5)
        assert response.status_code in (400, 404)
        print_test("Malformed Report ID (Path Traversal)", "PASS", "Correctly prevented path traversal")
        results["passed"] += 1
    except Exception as e:
        print_test("Malformed Report ID", "FAIL", str(e))
        results["failed"] += 1

    try:
        response = requests.get(f"{API_URL}/reports?skip=-5&limit=10", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["skip"] == 0
        print_test("Negative Skip Pagination", "PASS", "Correctly handled negative skip")
        results["passed"] += 1
    except Exception as e:
        print_test("Negative Skip Pagination", "FAIL", str(e))
        results["failed"] += 1

    try:
        response = requests.get(f"{API_URL}/reports?skip=0&limit=1000", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["limit"] <= 100
        print_test("Excessive Limit Pagination", "PASS", "Correctly capped limit at 100")
        results["passed"] += 1
    except Exception as e:
        print_test("Excessive Limit Pagination", "FAIL", str(e))
        results["failed"] += 1

    return results


def run_edge_case_tests() -> bool:
    """Run all edge case tests."""
    print(f"\n{BOLD}{GREEN}{'='*70}{RESET}")
    print(f"{BOLD}{GREEN}{'PHASE 5: EDGE CASE TESTING SUITE'.center(70)}{RESET}")
    print(f"{BOLD}{GREEN}{'='*70}{RESET}\n")

    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code != 200:
            print(f"{RED}❌ Backend server is not responding!{RESET}")
            sys.exit(1)
    except Exception:
        print(f"{RED}❌ Backend server is not running!{RESET}")
        print(f"{YELLOW}Please start the backend server first (in another terminal):{RESET}")
        print("  source venv/bin/activate   # or venv\\Scripts\\activate on Windows")
        print("  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        sys.exit(1)

    print(f"{GREEN}✅ Backend server is running{RESET}\n")

    all_results = {
        "File Upload": {"passed": 0, "failed": 0},
        "Job Description": {"passed": 0, "failed": 0},
        "Network": {"passed": 0, "failed": 0},
    }

    try:
        all_results["File Upload"] = test_file_upload_edge_cases()
    except Exception as e:
        print(f"{RED}File upload tests error: {e}{RESET}")
        all_results["File Upload"]["failed"] += 1

    try:
        all_results["Job Description"] = test_job_description_edge_cases()
    except Exception as e:
        print(f"{RED}Job description tests error: {e}{RESET}")
        all_results["Job Description"]["failed"] += 1

    try:
        all_results["Network"] = test_network_edge_cases()
    except Exception as e:
        print(f"{RED}Network tests error: {e}{RESET}")
        all_results["Network"]["failed"] += 1

    print_header("EDGE CASE TEST SUMMARY")
    total_passed = sum(r["passed"] for r in all_results.values())
    total_failed = sum(r["failed"] for r in all_results.values())

    for category, res in all_results.items():
        status = f"{GREEN}✅ PASS{RESET}" if res["failed"] == 0 else f"{RED}❌ FAIL{RESET}"
        print(f"{BOLD}{category}:{RESET} {status} ({res['passed']} passed, {res['failed']} failed)")

    print(f"\n{BOLD}Total:{RESET} {GREEN}{total_passed} passed{RESET}, {RED}{total_failed} failed{RESET}")

    if total_failed == 0:
        print(f"\n{BOLD}{GREEN}🎉 All edge case tests passed!{RESET}\n")
        return True
    print(f"\n{BOLD}{YELLOW}⚠️  Some edge case tests failed. Please review.{RESET}\n")
    return False


if __name__ == "__main__":
    try:
        success = run_edge_case_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Tests interrupted by user{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Unexpected error: {e}{RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
