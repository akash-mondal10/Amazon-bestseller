#!/usr/bin/env python3
"""
Comprehensive backend API testing for Amazon Best Seller Analyzer
Tests all endpoints to verify functionality and data integrity
"""

import requests
import sys
import json
from datetime import datetime

class AmazonAnalyzerAPITester:
    def __init__(self, base_url="https://reading-trends-hub.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def run_test(self, name, method, endpoint, expected_status=200, data=None, check_content=None):
        """Run a single API test with optional content validation"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")

            success = response.status_code == expected_status
            
            if success:
                try:
                    response_data = response.json()
                    
                    # Additional content checks
                    if check_content:
                        content_valid = check_content(response_data)
                        if not content_valid:
                            success = False
                            print(f"❌ Failed - Content validation failed")
                        else:
                            print(f"✅ Passed - Status: {response.status_code}, Content: Valid")
                    else:
                        print(f"✅ Passed - Status: {response.status_code}")
                    
                    if success:
                        self.tests_passed += 1
                        return True, response_data
                    else:
                        self.failed_tests.append(f"{name}: Content validation failed")
                        return False, {}
                        
                except json.JSONDecodeError:
                    if expected_status == 200:
                        print(f"❌ Failed - Invalid JSON response")
                        self.failed_tests.append(f"{name}: Invalid JSON response")
                        return False, {}
                    else:
                        # For file downloads, JSON decode error is expected
                        print(f"✅ Passed - Status: {response.status_code} (Binary response)")
                        self.tests_passed += 1
                        return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                self.failed_tests.append(f"{name}: Expected {expected_status}, got {response.status_code}")
                return False, {}

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed - Network Error: {str(e)}")
            self.failed_tests.append(f"{name}: Network error - {str(e)}")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append(f"{name}: Error - {str(e)}")
            return False, {}

    def test_summary_endpoint(self):
        """Test /api/summary - should show 550 total books"""
        def check_summary(data):
            if 'total_books' not in data:
                print(f"   Missing 'total_books' field")
                return False
            if data['total_books'] != 550:
                print(f"   Expected 550 books, got {data['total_books']}")
                return False
            required_fields = ['avg_rating', 'avg_price', 'total_reviews', 'genres', 'year_range']
            for field in required_fields:
                if field not in data:
                    print(f"   Missing required field: {field}")
                    return False
            print(f"   ✓ Total books: {data['total_books']}")
            print(f"   ✓ Avg rating: {data['avg_rating']}")
            print(f"   ✓ Genres: {len(data['genres'])}")
            return True
        
        return self.run_test("Summary Statistics", "GET", "summary", check_content=check_summary)

    def test_search_endpoint(self):
        """Test /api/search?q=harry - should return Harry Potter books"""
        def check_search(data):
            if 'results' not in data or 'total' not in data:
                print(f"   Missing 'results' or 'total' field")
                return False
            if data['total'] == 0:
                print(f"   No search results found for 'harry'")
                return False
            # Check if any result contains Harry Potter related content
            harry_found = False
            for book in data['results']:
                if 'harry' in book.get('Name', '').lower() or 'harry' in book.get('Author', '').lower():
                    harry_found = True
                    break
            if not harry_found:
                print(f"   No Harry Potter related books found in results")
                return False
            print(f"   ✓ Found {data['total']} results for 'harry'")
            print(f"   ✓ Sample result: {data['results'][0].get('Name', 'N/A')}")
            return True
        
        return self.run_test("Search Harry Potter", "GET", "search?q=harry", check_content=check_search)

    def test_ml_predict_endpoint(self):
        """Test /api/ml/predict with POST {price:14,year:2020,genre:Fiction}"""
        test_data = {"price": 14, "year": 2020, "genre": "Fiction"}
        
        def check_prediction(data):
            required_fields = ['bestseller_prediction', 'rating_prediction', 'input']
            for field in required_fields:
                if field not in data:
                    print(f"   Missing required field: {field}")
                    return False
            
            # Check bestseller prediction structure
            bs_pred = data['bestseller_prediction']
            if 'is_bestseller' not in bs_pred or 'probability' not in bs_pred:
                print(f"   Invalid bestseller prediction structure")
                return False
            
            # Check rating prediction structure
            rating_pred = data['rating_prediction']
            if 'predicted_rating' not in rating_pred:
                print(f"   Invalid rating prediction structure")
                return False
            
            print(f"   ✓ Bestseller: {bs_pred['is_bestseller']} (prob: {bs_pred['probability']:.3f})")
            print(f"   ✓ Rating: {rating_pred['predicted_rating']}")
            return True
        
        return self.run_test("ML Prediction", "POST", "ml/predict", data=test_data, check_content=check_prediction)

    def test_ml_info_endpoint(self):
        """Test /api/ml/info - should return model metrics"""
        def check_ml_info(data):
            required_fields = ['classification', 'regression', 'features_used', 'dataset_size']
            for field in required_fields:
                if field not in data:
                    print(f"   Missing required field: {field}")
                    return False
            
            if data['dataset_size'] != 550:
                print(f"   Expected dataset size 550, got {data['dataset_size']}")
                return False
            
            print(f"   ✓ Dataset size: {data['dataset_size']}")
            print(f"   ✓ Classification model: {data['classification']['model']}")
            print(f"   ✓ Regression model: {data['regression']['model']}")
            return True
        
        return self.run_test("ML Model Info", "GET", "ml/info", check_content=check_ml_info)

    def test_export_endpoints(self):
        """Test export endpoints - should return downloadable files"""
        # Test Excel export - expect binary response, not JSON
        print(f"\n🔍 Testing Export Excel...")
        try:
            url = f"{self.api_url}/export/excel"
            response = requests.get(url, timeout=30)
            if response.status_code == 200 and 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in response.headers.get('content-type', ''):
                print(f"✅ Passed - Excel export working (binary file)")
                self.tests_passed += 1
                excel_success = True
            else:
                print(f"❌ Failed - Excel export issue: {response.status_code}")
                self.failed_tests.append("Export Excel: Invalid response")
                excel_success = False
        except Exception as e:
            print(f"❌ Failed - Excel export error: {str(e)}")
            self.failed_tests.append(f"Export Excel: {str(e)}")
            excel_success = False
        self.tests_run += 1
        
        # Test PDF export - expect binary response, not JSON
        print(f"\n🔍 Testing Export PDF...")
        try:
            url = f"{self.api_url}/export/pdf"
            response = requests.get(url, timeout=30)
            if response.status_code == 200 and 'application/pdf' in response.headers.get('content-type', ''):
                print(f"✅ Passed - PDF export working (binary file)")
                self.tests_passed += 1
                pdf_success = True
            else:
                print(f"❌ Failed - PDF export issue: {response.status_code}")
                self.failed_tests.append("Export PDF: Invalid response")
                pdf_success = False
        except Exception as e:
            print(f"❌ Failed - PDF export error: {str(e)}")
            self.failed_tests.append(f"Export PDF: {str(e)}")
            pdf_success = False
        self.tests_run += 1
        
        return excel_success and pdf_success

    def test_top_authors_endpoint(self):
        """Test /api/top-authors - should return top 10 authors"""
        def check_authors(data):
            if 'authors' not in data or 'counts' not in data:
                print(f"   Missing 'authors' or 'counts' field")
                return False
            if len(data['authors']) != 10:
                print(f"   Expected 10 authors, got {len(data['authors'])}")
                return False
            print(f"   ✓ Top author: {data['authors'][0]} ({data['counts'][0]} books)")
            return True
        
        return self.run_test("Top Authors", "GET", "top-authors", check_content=check_authors)

    def test_books_search_endpoint(self):
        """Test /api/books?search=rowling - should support search parameter"""
        def check_books_search(data):
            if 'books' not in data or 'total' not in data:
                print(f"   Missing 'books' or 'total' field")
                return False
            if data['total'] == 0:
                print(f"   No books found for 'rowling' search")
                return False
            # Check if results contain Rowling
            rowling_found = False
            for book in data['books']:
                if 'rowling' in book.get('Author', '').lower():
                    rowling_found = True
                    break
            if not rowling_found:
                print(f"   No Rowling books found in search results")
                return False
            print(f"   ✓ Found {data['total']} books by Rowling")
            return True
        
        return self.run_test("Books Search Rowling", "GET", "books?search=rowling", check_content=check_books_search)

    def test_additional_endpoints(self):
        """Test additional endpoints for completeness"""
        endpoints = [
            ("Root API", ""),
            ("Genre Distribution", "genre-distribution"),
            ("Year Trends", "year-trends"),
            ("Price Rating", "price-rating"),
            ("Correlation", "correlation"),
            ("Filter Options", "filter-options"),
            ("Insights", "insights")
        ]
        
        all_passed = True
        for name, endpoint in endpoints:
            success, _ = self.run_test(name, "GET", endpoint)
            if not success:
                all_passed = False
        
        return all_passed

def main():
    print("🚀 Starting Amazon Best Seller Analyzer API Tests")
    print("=" * 60)
    
    tester = AmazonAnalyzerAPITester()
    
    # Core functionality tests
    print("\n📊 CORE FUNCTIONALITY TESTS")
    print("-" * 40)
    
    summary_ok = tester.test_summary_endpoint()
    search_ok = tester.test_search_endpoint()
    ml_predict_ok = tester.test_ml_predict_endpoint()
    ml_info_ok = tester.test_ml_info_endpoint()
    export_ok = tester.test_export_endpoints()
    authors_ok = tester.test_top_authors_endpoint()
    books_search_ok = tester.test_books_search_endpoint()
    
    # Additional endpoints
    print("\n🔧 ADDITIONAL ENDPOINTS")
    print("-" * 40)
    additional_ok = tester.test_additional_endpoints()
    
    # Results summary
    print("\n" + "=" * 60)
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Tests Failed: {tester.tests_run - tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed / tester.tests_run * 100):.1f}%")
    
    if tester.failed_tests:
        print("\n❌ FAILED TESTS:")
        for i, failure in enumerate(tester.failed_tests, 1):
            print(f"   {i}. {failure}")
    
    # Critical functionality check
    critical_tests = [summary_ok, search_ok, ml_predict_ok, ml_info_ok, authors_ok, books_search_ok]
    critical_passed = sum(1 for test in critical_tests if test)
    
    print(f"\n🎯 CRITICAL FUNCTIONALITY: {critical_passed}/6 tests passed")
    
    if critical_passed >= 5:
        print("✅ Backend is functioning well - ready for frontend testing")
        return 0
    elif critical_passed >= 3:
        print("⚠️  Backend has some issues but core functionality works")
        return 1
    else:
        print("❌ Backend has major issues - needs fixing before frontend testing")
        return 2

if __name__ == "__main__":
    sys.exit(main())