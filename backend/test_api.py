"""
Simple script to test the Flask API endpoints
Run this after starting the Flask server to verify it's working
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_root():
    """Test root endpoint"""
    print("Testing root endpoint (GET /)...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Root endpoint working!\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint (GET /api/health)...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Health endpoint working!\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

def test_generate():
    """Test generate endpoint (requires API key)"""
    print("Testing generate endpoint (POST /api/generate)...")
    print("Note: This requires a valid OpenAI API key in .env file\n")
    
    # You can uncomment and add your test data here
    # test_data = {
    #     "date": "2025-01-10",
    #     "summary": "Worked on implementing a REST API, reviewed code with team"
    # }
    # 
    # try:
    #     response = requests.post(f"{BASE_URL}/api/generate", json=test_data)
    #     print(f"Status: {response.status_code}")
    #     if response.status_code == 200:
    #         print("✅ Generate endpoint working!")
    #     else:
    #         print(f"Response: {json.dumps(response.json(), indent=2)}")
    # except Exception as e:
    #     print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 Testing Flask API Endpoints")
    print("=" * 50)
    print("Make sure the Flask server is running on http://localhost:5000\n")
    
    test_root()
    test_health()
    test_generate()
    
    print("=" * 50)
    print("✅ Testing complete!")
    print("=" * 50)

