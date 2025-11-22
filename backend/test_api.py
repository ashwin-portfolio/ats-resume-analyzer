"""
Simple test script to verify API is working
Run this after starting the server
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("🧪 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/api/v1/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✅ Health check passed!\n")

def test_root():
    """Test root endpoint"""
    print("🧪 Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✅ Root endpoint passed!\n")

def test_analyze_mock():
    """Test analyze endpoint with mock data"""
    print("🧪 Testing analyze endpoint (mock)...")
    
    # Create a dummy file
    files = {
        'resume_file': ('test_resume.pdf', b'dummy pdf content', 'application/pdf')
    }
    data = {
        'job_description': 'Looking for a Python developer with FastAPI experience'
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/analyze", files=files, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("✅ Analyze endpoint passed!\n")

if __name__ == "__main__":
    print("=" * 50)
    print("ATS Resume Analyzer - API Test Suite")
    print("=" * 50 + "\n")
    
    try:
        test_root()
        test_health()
        test_analyze_mock()
        print("\n🎉 All tests passed!")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server.")
        print("Make sure the server is running on http://localhost:8000")
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

