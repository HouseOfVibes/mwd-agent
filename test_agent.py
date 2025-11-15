#!/usr/bin/env python3
"""
Test script for MWD Agent
Tests all endpoints with sample client data
"""

import requests
import json

BASE_URL = "http://localhost:8080"

# Sample client data
SAMPLE_CLIENT = {
    "company_name": "TechFlow Solutions",
    "industry": "B2B SaaS",
    "target_audience": "Mid-size tech companies looking to streamline their workflow",
    "key_services": [
        "Project management software",
        "Team collaboration tools",
        "Analytics dashboard"
    ],
    "brand_values": [
        "Innovation",
        "Simplicity",
        "Reliability"
    ],
    "competitors": [
        "Asana",
        "Monday.com",
        "Trello"
    ],
    "unique_selling_point": "AI-powered automation that learns from your team's workflow"
}


def test_endpoint(endpoint_name, endpoint_path, client_data):
    """Test a single endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {endpoint_name}")
    print(f"{'='*60}")

    try:
        response = requests.post(
            f"{BASE_URL}{endpoint_path}",
            json=client_data,
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()

            if result.get('success'):
                print(f"\n✅ Success!")
                print(f"\nResponse Preview:")
                print("-" * 60)
                # Show first 500 characters of response
                response_text = result['response'][:500]
                print(response_text)
                if len(result['response']) > 500:
                    print("\n... (truncated)")

                print(f"\n📊 Token Usage:")
                print(f"  Input tokens: {result['usage']['input_tokens']}")
                print(f"  Output tokens: {result['usage']['output_tokens']}")
            else:
                print(f"\n❌ Error: {result.get('error')}")
        else:
            print(f"\n❌ HTTP Error: {response.status_code}")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print(f"\n❌ Connection Error: Make sure main.py is running!")
    except requests.exceptions.Timeout:
        print(f"\n❌ Timeout: Request took too long")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")


def main():
    print("\n" + "="*60)
    print("🧪 MWD Agent - Test Suite")
    print("="*60)
    print(f"\nTarget: {BASE_URL}")
    print(f"\nClient: {SAMPLE_CLIENT['company_name']}")

    # Check if server is running
    try:
        response = requests.get(BASE_URL)
        status = response.json()
        print(f"\n✅ Server is running")
        print(f"   Config: {status['config']}")
    except:
        print(f"\n❌ Server is not running!")
        print(f"\nPlease start the server first:")
        print(f"  python main.py")
        return

    # Test each endpoint
    endpoints = [
        ("Branding Strategy", "/branding"),
        ("Website Design", "/website"),
        ("Social Media Strategy", "/social"),
        ("Copywriting", "/copywriting")
    ]

    for name, path in endpoints:
        test_endpoint(name, path, SAMPLE_CLIENT)
        print()  # Extra spacing between tests

    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
