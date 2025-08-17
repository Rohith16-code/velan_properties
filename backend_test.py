#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for Velan Properties
Tests Contact Form API, Properties API, and Property CRUD Operations
"""

import requests
import json
import uuid
from datetime import datetime
import time

# Configuration
BASE_URL = "https://trusted-estates.preview.emergentagent.com/api"
TIMEOUT = 30

class VelanPropertiesAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.timeout = TIMEOUT
        self.test_results = {
            "contact_form_api": {"passed": 0, "failed": 0, "details": []},
            "properties_api": {"passed": 0, "failed": 0, "details": []},
            "property_crud": {"passed": 0, "failed": 0, "details": []}
        }
        
    def log_result(self, category, test_name, passed, details=""):
        """Log test result"""
        if passed:
            self.test_results[category]["passed"] += 1
            status = "✅ PASS"
        else:
            self.test_results[category]["failed"] += 1
            status = "❌ FAIL"
            
        self.test_results[category]["details"].append(f"{status}: {test_name} - {details}")
        print(f"{status}: {test_name} - {details}")
        
    def test_health_check(self):
        """Test API health check"""
        print("\n=== Testing API Health Check ===")
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    print("✅ API Health Check: Backend is healthy and responding")
                    return True
                else:
                    print(f"❌ API Health Check: Unexpected response - {data}")
                    return False
            else:
                print(f"❌ API Health Check: HTTP {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ API Health Check: Connection failed - {str(e)}")
            return False
    
    def test_contact_form_api(self):
        """Test Contact Form API with various scenarios"""
        print("\n=== Testing Contact Form API ===")
        
        # Test 1: Valid contact submission
        valid_contact = {
            "name": "Rajesh Kumar",
            "email": "rajesh.kumar@example.com",
            "phone": "+919876543210",
            "message": "I am interested in purchasing a 3BHK villa in Hosur. Please contact me with available options and pricing details."
        }
        
        try:
            response = self.session.post(f"{self.base_url}/contacts", json=valid_contact)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("contact_id"):
                    self.log_result("contact_form_api", "Valid Contact Submission", True, 
                                  f"Contact created with ID: {data.get('contact_id')}")
                else:
                    self.log_result("contact_form_api", "Valid Contact Submission", False, 
                                  f"Invalid response structure: {data}")
            else:
                self.log_result("contact_form_api", "Valid Contact Submission", False, 
                              f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_result("contact_form_api", "Valid Contact Submission", False, str(e))
        
        # Test 2: Invalid email format
        invalid_email_contact = {
            "name": "Priya Sharma",
            "email": "invalid-email-format",
            "phone": "+919123456789",
            "message": "Looking for rental properties in Hosur area with good connectivity to Bangalore."
        }
        
        try:
            response = self.session.post(f"{self.base_url}/contacts", json=invalid_email_contact)
            if response.status_code == 422:  # Validation error expected
                self.log_result("contact_form_api", "Invalid Email Format", True, 
                              "Correctly rejected invalid email format")
            else:
                self.log_result("contact_form_api", "Invalid Email Format", False, 
                              f"Should reject invalid email, got HTTP {response.status_code}")
        except Exception as e:
            self.log_result("contact_form_api", "Invalid Email Format", False, str(e))
        
        # Test 3: Missing required fields
        missing_fields_contact = {
            "name": "Arun Patel",
            "email": "arun.patel@example.com"
            # Missing message field
        }
        
        try:
            response = self.session.post(f"{self.base_url}/contacts", json=missing_fields_contact)
            if response.status_code == 422:  # Validation error expected
                self.log_result("contact_form_api", "Missing Required Fields", True, 
                              "Correctly rejected missing message field")
            else:
                self.log_result("contact_form_api", "Missing Required Fields", False, 
                              f"Should reject missing fields, got HTTP {response.status_code}")
        except Exception as e:
            self.log_result("contact_form_api", "Missing Required Fields", False, str(e))
        
        # Test 4: Very long message (boundary testing)
        long_message_contact = {
            "name": "Deepika Reddy",
            "email": "deepika.reddy@example.com",
            "phone": "+919988776655",
            "message": "A" * 1500  # Exceeds 1000 character limit
        }
        
        try:
            response = self.session.post(f"{self.base_url}/contacts", json=long_message_contact)
            if response.status_code == 422:  # Validation error expected
                self.log_result("contact_form_api", "Message Length Validation", True, 
                              "Correctly rejected message exceeding 1000 characters")
            else:
                self.log_result("contact_form_api", "Message Length Validation", False, 
                              f"Should reject long message, got HTTP {response.status_code}")
        except Exception as e:
            self.log_result("contact_form_api", "Message Length Validation", False, str(e))
        
        # Test 5: Short name validation
        short_name_contact = {
            "name": "A",  # Too short (min 2 characters)
            "email": "test@example.com",
            "message": "Interested in properties near Hosur railway station."
        }
        
        try:
            response = self.session.post(f"{self.base_url}/contacts", json=short_name_contact)
            if response.status_code == 422:  # Validation error expected
                self.log_result("contact_form_api", "Name Length Validation", True, 
                              "Correctly rejected name shorter than 2 characters")
            else:
                self.log_result("contact_form_api", "Name Length Validation", False, 
                              f"Should reject short name, got HTTP {response.status_code}")
        except Exception as e:
            self.log_result("contact_form_api", "Name Length Validation", False, str(e))
    
    def test_properties_api(self):
        """Test Properties API with different query parameters"""
        print("\n=== Testing Properties API ===")
        
        # Test 1: Get all properties (default)
        try:
            response = self.session.get(f"{self.base_url}/properties")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    # Verify property structure
                    property_sample = data[0]
                    required_fields = ["id", "title", "price", "location", "bedrooms", "parking", "area", "type"]
                    if all(field in property_sample for field in required_fields):
                        self.log_result("properties_api", "Get All Properties", True, 
                                      f"Retrieved {len(data)} properties with correct structure")
                    else:
                        missing = [f for f in required_fields if f not in property_sample]
                        self.log_result("properties_api", "Get All Properties", False, 
                                      f"Missing fields in property: {missing}")
                else:
                    self.log_result("properties_api", "Get All Properties", False, 
                                  f"Expected list with properties, got: {type(data)}")
            else:
                self.log_result("properties_api", "Get All Properties", False, 
                              f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_result("properties_api", "Get All Properties", False, str(e))
        
        # Test 2: Properties with pagination
        try:
            response = self.session.get(f"{self.base_url}/properties?limit=2&offset=0")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) <= 2:
                    self.log_result("properties_api", "Properties Pagination", True, 
                                  f"Pagination working, got {len(data)} properties (limit=2)")
                else:
                    self.log_result("properties_api", "Properties Pagination", False, 
                                  f"Pagination failed, expected ≤2 properties, got {len(data)}")
            else:
                self.log_result("properties_api", "Properties Pagination", False, 
                              f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_result("properties_api", "Properties Pagination", False, str(e))
        
        # Test 3: Filter by property type
        for property_type in ["For Sale", "For Rent", "Investment"]:
            try:
                response = self.session.get(f"{self.base_url}/properties?type={property_type}")
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        # Check if all returned properties match the filter
                        if len(data) == 0 or all(prop.get("type") == property_type for prop in data):
                            self.log_result("properties_api", f"Filter by Type ({property_type})", True, 
                                          f"Filter working, got {len(data)} properties")
                        else:
                            wrong_types = [prop.get("type") for prop in data if prop.get("type") != property_type]
                            self.log_result("properties_api", f"Filter by Type ({property_type})", False, 
                                          f"Filter failed, found wrong types: {wrong_types}")
                    else:
                        self.log_result("properties_api", f"Filter by Type ({property_type})", False, 
                                      f"Expected list, got: {type(data)}")
                else:
                    self.log_result("properties_api", f"Filter by Type ({property_type})", False, 
                                  f"HTTP {response.status_code}: {response.text}")
            except Exception as e:
                self.log_result("properties_api", f"Filter by Type ({property_type})", False, str(e))
        
        # Test 4: Invalid pagination parameters
        try:
            response = self.session.get(f"{self.base_url}/properties?limit=-1")
            if response.status_code == 422:  # Validation error expected
                self.log_result("properties_api", "Invalid Pagination Parameters", True, 
                              "Correctly rejected negative limit")
            else:
                self.log_result("properties_api", "Invalid Pagination Parameters", False, 
                              f"Should reject negative limit, got HTTP {response.status_code}")
        except Exception as e:
            self.log_result("properties_api", "Invalid Pagination Parameters", False, str(e))
    
    def test_property_crud_operations(self):
        """Test Property CRUD Operations"""
        print("\n=== Testing Property CRUD Operations ===")
        
        # Test 1: Create new property
        test_property = {
            "title": "Test Property - Modern Apartment",
            "price": "₹35,00,000",
            "location": "Electronic City, Hosur",
            "bedrooms": 3,
            "parking": 2,
            "area": "1,800 sq ft",
            "type": "For Sale",
            "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
            "description": "Modern apartment with excellent connectivity to Bangalore and all modern amenities.",
            "features": ["Gym", "Swimming Pool", "Security", "Power Backup", "Elevator"]
        }
        
        created_property_id = None
        try:
            response = self.session.post(f"{self.base_url}/properties", json=test_property)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("property_id"):
                    created_property_id = data.get("property_id")
                    self.log_result("property_crud", "Create Property", True, 
                                  f"Property created with ID: {created_property_id}")
                else:
                    self.log_result("property_crud", "Create Property", False, 
                                  f"Invalid response structure: {data}")
            else:
                self.log_result("property_crud", "Create Property", False, 
                              f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_result("property_crud", "Create Property", False, str(e))
        
        # Test 2: Create property with invalid data
        invalid_property = {
            "title": "A",  # Too short
            "price": "",   # Empty
            "location": "Test Location",
            "bedrooms": 0,  # Below minimum
            "parking": -1,  # Below minimum
            "area": "1000 sq ft",
            "type": "Invalid Type",  # Not in allowed values
            "image": "short"  # Too short
        }
        
        try:
            response = self.session.post(f"{self.base_url}/properties", json=invalid_property)
            if response.status_code == 422:  # Validation error expected
                self.log_result("property_crud", "Create Property Validation", True, 
                              "Correctly rejected invalid property data")
            else:
                self.log_result("property_crud", "Create Property Validation", False, 
                              f"Should reject invalid data, got HTTP {response.status_code}")
        except Exception as e:
            self.log_result("property_crud", "Create Property Validation", False, str(e))
        
        # Test 3: Update property (if we created one successfully)
        if created_property_id:
            update_data = {
                "price": "₹38,00,000",
                "description": "Updated description - Price negotiable for immediate sale.",
                "status": "active"
            }
            
            try:
                response = self.session.put(f"{self.base_url}/properties/{created_property_id}", json=update_data)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        self.log_result("property_crud", "Update Property", True, 
                                      f"Property {created_property_id} updated successfully")
                    else:
                        self.log_result("property_crud", "Update Property", False, 
                                      f"Update failed: {data}")
                else:
                    self.log_result("property_crud", "Update Property", False, 
                                  f"HTTP {response.status_code}: {response.text}")
            except Exception as e:
                self.log_result("property_crud", "Update Property", False, str(e))
        
        # Test 4: Update non-existent property
        fake_id = str(uuid.uuid4())
        try:
            response = self.session.put(f"{self.base_url}/properties/{fake_id}", json={"price": "₹50,00,000"})
            if response.status_code == 404:  # Not found expected
                self.log_result("property_crud", "Update Non-existent Property", True, 
                              "Correctly returned 404 for non-existent property")
            else:
                self.log_result("property_crud", "Update Non-existent Property", False, 
                              f"Should return 404, got HTTP {response.status_code}")
        except Exception as e:
            self.log_result("property_crud", "Update Non-existent Property", False, str(e))
        
        # Test 5: Delete property (if we created one)
        if created_property_id:
            try:
                response = self.session.delete(f"{self.base_url}/properties/{created_property_id}")
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        self.log_result("property_crud", "Delete Property", True, 
                                      f"Property {created_property_id} deleted successfully")
                    else:
                        self.log_result("property_crud", "Delete Property", False, 
                                      f"Delete failed: {data}")
                else:
                    self.log_result("property_crud", "Delete Property", False, 
                                  f"HTTP {response.status_code}: {response.text}")
            except Exception as e:
                self.log_result("property_crud", "Delete Property", False, str(e))
        
        # Test 6: Delete non-existent property
        fake_id = str(uuid.uuid4())
        try:
            response = self.session.delete(f"{self.base_url}/properties/{fake_id}")
            if response.status_code == 404:  # Not found expected
                self.log_result("property_crud", "Delete Non-existent Property", True, 
                              "Correctly returned 404 for non-existent property")
            else:
                self.log_result("property_crud", "Delete Non-existent Property", False, 
                              f"Should return 404, got HTTP {response.status_code}")
        except Exception as e:
            self.log_result("property_crud", "Delete Non-existent Property", False, str(e))
    
    def test_admin_dashboard(self):
        """Test admin dashboard endpoint"""
        print("\n=== Testing Admin Dashboard ===")
        try:
            response = self.session.get(f"{self.base_url}/admin/dashboard")
            if response.status_code == 200:
                data = response.json()
                if "contacts" in data and "properties" in data:
                    contacts = data["contacts"]
                    properties = data["properties"]
                    if "total" in contacts and "total" in properties:
                        print(f"✅ Admin Dashboard: Retrieved stats - Contacts: {contacts['total']}, Properties: {properties['total']}")
                        return True
                    else:
                        print(f"❌ Admin Dashboard: Missing stats fields - {data}")
                        return False
                else:
                    print(f"❌ Admin Dashboard: Invalid response structure - {data}")
                    return False
            else:
                print(f"❌ Admin Dashboard: HTTP {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Admin Dashboard: {str(e)}")
            return False
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("VELAN PROPERTIES BACKEND API TEST SUMMARY")
        print("="*60)
        
        total_passed = 0
        total_failed = 0
        
        for category, results in self.test_results.items():
            passed = results["passed"]
            failed = results["failed"]
            total_passed += passed
            total_failed += failed
            
            category_name = category.replace("_", " ").title()
            print(f"\n{category_name}:")
            print(f"  ✅ Passed: {passed}")
            print(f"  ❌ Failed: {failed}")
            
            if results["details"]:
                print("  Details:")
                for detail in results["details"]:
                    print(f"    {detail}")
        
        print(f"\nOVERALL RESULTS:")
        print(f"✅ Total Passed: {total_passed}")
        print(f"❌ Total Failed: {total_failed}")
        print(f"📊 Success Rate: {(total_passed/(total_passed+total_failed)*100):.1f}%" if (total_passed+total_failed) > 0 else "No tests run")
        
        return total_failed == 0
    
    def run_all_tests(self):
        """Run all backend API tests"""
        print("Starting Velan Properties Backend API Tests...")
        print(f"Testing against: {self.base_url}")
        
        # Health check first
        if not self.test_health_check():
            print("❌ Backend API is not responding. Aborting tests.")
            return False
        
        # Run all test suites
        self.test_contact_form_api()
        self.test_properties_api()
        self.test_property_crud_operations()
        self.test_admin_dashboard()
        
        # Print summary
        return self.print_summary()

if __name__ == "__main__":
    tester = VelanPropertiesAPITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! Backend API is working correctly.")
        exit(0)
    else:
        print("\n⚠️  Some tests failed. Check the details above.")
        exit(1)