"""
API tests for Anagram Checker
"""
import pytest
import allure
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@allure.feature('Anagram Checker API')
@allure.story('API Endpoints')
@pytest.mark.api
class TestAnagramAPI:
    """Test cases for API endpoints"""

    @allure.title("Test health check endpoint")
    def test_health_check(self, client):
        """Test the health check endpoint"""
        with allure.step("GET /health"):
            response = client.get("/health")

        with allure.step("Verify response"):
            assert response.status_code == 200
            assert response.json() == {"status": "healthy"}

    @allure.title("Test root endpoint returns HTML")
    def test_root_endpoint(self, client):
        """Test that root endpoint returns HTML page"""
        with allure.step("GET /"):
            response = client.get("/")

        with allure.step("Verify response"):
            assert response.status_code == 200
            assert "text/html" in response.headers["content-type"]
            assert "Anagram Checker" in response.text

    @allure.title("Test API check endpoint with valid anagrams")
    @pytest.mark.parametrize("input1,input2,expected", [
        ("listen", "silent", True),
        ("A gentleman", "Elegant Man", True),
        ("school master", "the classroom", True),
        ("conversation", "voices rant on", True),
        ("eleven plus two", "twelve plus one", True),
        ("apple", "paple", True),
    ])
    def test_check_anagrams_api(self, client, input1, input2, expected):
        """Test API endpoint with valid anagrams"""
        with allure.step(f"POST /api/check with '{input1}' and '{input2}'"):
            response = client.post(
                "/api/check",
                json={"input1": input1, "input2": input2}
            )

        with allure.step("Verify response"):
            assert response.status_code == 200
            data = response.json()
            assert data["input1"] == input1
            assert data["input2"] == input2
            assert data["result"] == expected

        allure.attach(
            f"Request: {input1}, {input2}\nResponse: {data['result']}",
            name="API Test Details",
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.title("Test API check endpoint with non-anagrams")
    @pytest.mark.parametrize("input1,input2,expected", [
        ("hello", "world", False),
        ("rat", "car", False),
    ])
    def test_check_non_anagrams_api(self, client, input1, input2, expected):
        """Test API endpoint with non-anagrams"""
        with allure.step(f"POST /api/check with '{input1}' and '{input2}'"):
            response = client.post(
                "/api/check",
                json={"input1": input1, "input2": input2}
            )

        with allure.step("Verify response"):
            assert response.status_code == 200
            data = response.json()
            assert data["result"] == expected

    @allure.title("Test API with empty input")
    def test_api_empty_input(self, client):
        """Test API with empty input strings"""
        with allure.step("POST /api/check with empty strings"):
            response = client.post(
                "/api/check",
                json={"input1": "", "input2": ""}
            )

        # Empty strings should fail validation
        assert response.status_code == 422

    @allure.title("Test API with missing fields")
    def test_api_missing_fields(self, client):
        """Test API with missing required fields"""
        with allure.step("POST /api/check with missing input2"):
            response = client.post(
                "/api/check",
                json={"input1": "test"}
            )

        with allure.step("Verify validation error"):
            assert response.status_code == 422

    @allure.title("Test API with invalid JSON")
    def test_api_invalid_json(self, client):
        """Test API with invalid JSON"""
        with allure.step("POST /api/check with invalid JSON"):
            response = client.post(
                "/api/check",
                data="invalid json",
                headers={"Content-Type": "application/json"}
            )

        with allure.step("Verify error response"):
            assert response.status_code == 422

    @allure.title("Test OpenAPI documentation")
    def test_openapi_docs(self, client):
        """Test that OpenAPI docs are available"""
        with allure.step("GET /docs"):
            response = client.get("/docs")

        with allure.step("Verify docs are available"):
            assert response.status_code == 200


@allure.feature('Anagram Checker API')
@allure.story('BDD API Tests')
@pytest.mark.api
@pytest.mark.bdd
class TestAnagramAPIBDD:
    """BDD-style API tests"""

    @allure.title("BDD: Check if two strings are anagrams via API")
    @pytest.mark.parametrize("input1,input2,output", [
        ("listen", "silent", "true"),
        ("hello", "world", "false"),
        ("conversation", "voices rant on", "true"),
        ("school master", "the classroom", "true"),
        ("a gentleman", "elegant man", "true"),
        ("eleven plus two", "twelve plus one", "true"),
        ("apple", "paple", "true"),
        ("rat", "car", "false"),
    ])
    def test_bdd_api_anagram_check(self, client, input1, input2, output):
        """BDD: Given inputs, when checking via API, then result matches expected"""
        expected = output.lower() == "true"

        with allure.step(f"Given the input strings '{input1}' and '{input2}'"):
            request_data = {"input1": input1, "input2": input2}

        with allure.step("When I check if they are anagrams via API"):
            response = client.post("/api/check", json=request_data)

        with allure.step(f"Then the result should be '{output}'"):
            assert response.status_code == 200
            data = response.json()
            assert data["result"] == expected

        allure.attach(
            f"Input 1: {input1}\nInput 2: {input2}\nExpected: {output}\nActual: {data['result']}",
            name="BDD API Test Summary",
            attachment_type=allure.attachment_type.TEXT
        )
