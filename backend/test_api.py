#!/usr/bin/env python3
"""
Test script for the SoundCheck API
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_model_info():
    """Test the model info endpoint"""
    print("\nTesting model info endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/model/info")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Model info test failed: {e}")
        return False

def test_audio_generation():
    """Test audio generation endpoint"""
    print("\nTesting audio generation...")
    try:
        payload = {
            "frequency": 1000,
            "duration": 1.0,
            "volume": 0.5,
            "sample_rate": 44100
        }
        response = requests.post(f"{BASE_URL}/audio/generate", json=payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        print(f"Audio data length: {len(result.get('audio_data', ''))}")
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Audio generation test failed: {e}")
        return False

def test_hearing_analysis():
    """Test hearing test analysis endpoint"""
    print("\nTesting hearing test analysis...")
    try:
        # Sample hearing test data
        payload = {
            "user_info": {
                "age": 35,
                "gender": "Male"
            },
            "frequency_responses": [
                {"frequency": 500, "heard": True},
                {"frequency": 1000, "heard": True},
                {"frequency": 2000, "heard": True},
                {"frequency": 3000, "heard": False},
                {"frequency": 4000, "heard": False},
                {"frequency": 6000, "heard": False},
                {"frequency": 8000, "heard": False}
            ],
            "test_id": "test_001"
        }
        
        response = requests.post(f"{BASE_URL}/test/analyze", json=payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message')}")
        
        if result.get('result'):
            test_result = result['result']
            print(f"Predicted Category: {test_result.get('predicted_category')}")
            print(f"Confidence: {test_result.get('confidence_score'):.3f}")
            print(f"PTA Score: {test_result.get('pta_score'):.1f} dB HL")
            print(f"Risk Level: {test_result.get('risk_level')}")
            print(f"Recommendations: {len(test_result.get('recommendations', []))} items")
        
        return response.status_code == 200 and result.get('success')
    except Exception as e:
        print(f"Hearing analysis test failed: {e}")
        return False

def test_frequencies_endpoint():
    """Test the frequencies endpoint"""
    print("\nTesting frequencies endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/test/frequencies")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Frequencies: {result.get('frequencies')}")
        print(f"PTA Frequencies: {result.get('pta_frequencies')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Frequencies test failed: {e}")
        return False

def test_categories_endpoint():
    """Test the categories endpoint"""
    print("\nTesting categories endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/categories")
        print(f"Status: {response.status_code}")
        result = response.json()
        categories = result.get('categories', {})
        print(f"Available categories: {list(categories.keys())}")
        return response.status_code == 200
    except Exception as e:
        print(f"Categories test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Starting SoundCheck API Tests")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Model Info", test_model_info),
        ("Audio Generation", test_audio_generation),
        ("Hearing Analysis", test_hearing_analysis),
        ("Frequencies", test_frequencies_endpoint),
        ("Categories", test_categories_endpoint)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))
        print(f"Result: {'PASS' if success else 'FAIL'}")
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{test_name:20} : {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("❌ Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
