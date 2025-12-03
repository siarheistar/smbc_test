"""
API tests for Anagram Checker - Comprehensive test coverage
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
@allure.story('Comprehensive API Testing')
@pytest.mark.api
class TestAnagramAPI:
    """Comprehensive test cases for all API scenarios"""

    # ==================== Health & Documentation Tests ====================
    
    @allure.title("Test health check endpoint")
    def test_health_check(self, client):
        """Test the health check endpoint"""
        with allure.step("GET /health"):
            response = client.get("/health")

        with allure.step("Verify response"):
            assert response.status_code == 200
            data = response.json()
            assert response.status_code == 200
            assert data["status"] == "healthy"
            assert "environment" in data
            assert "version" in data

    @allure.title("Test root endpoint returns HTML")
    def test_root_endpoint(self, client):
        """Test that root endpoint returns HTML page"""
        with allure.step("GET /"):
            response = client.get("/")

        with allure.step("Verify response"):
            assert response.status_code == 200
            assert "text/html" in response.headers["content-type"]
            assert "Anagram Checker" in response.text

    @allure.title("Test OpenAPI documentation")
    def test_openapi_docs(self, client):
        """Test that OpenAPI docs are available"""
        with allure.step("GET /docs"):
            response = client.get("/docs")

        with allure.step("Verify docs are available"):
            assert response.status_code == 200

    @allure.title("Test ReDoc documentation")
    def test_redoc_docs(self, client):
        """Test that ReDoc docs are available"""
        with allure.step("GET /redoc"):
            response = client.get("/redoc")

        with allure.step("Verify ReDoc is available"):
            assert response.status_code == 200
            assert "redoc" in response.text.lower()

    @allure.title("Test OpenAPI JSON schema")
    def test_openapi_json(self, client):
        """Test that OpenAPI JSON schema is available"""
        with allure.step("GET /openapi.json"):
            response = client.get("/openapi.json")

        with allure.step("Verify OpenAPI schema"):
            assert response.status_code == 200
            data = response.json()
            assert "openapi" in data
            assert data["info"]["title"] == "Anagram Checker API"

    # ==================== Basic Anagram Tests ====================
    
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

    # ==================== Validation Error Tests ====================
    
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

    # ==================== Special Characters Tests ====================
    
    @allure.title("Test API with special characters")
    @pytest.mark.parametrize("input1,input2,expected", [
        ("hello!", "!olleh", True),  # Exclamation marks
        ("test@123", "123@test", True),  # @ symbol and numbers
        ("a-b-c", "c-b-a", True),  # Hyphens
        ("hello_world", "world_hello", True),  # Underscores
        ("test#tag", "gat#test", True),  # Hash symbol
        ("a$b$c", "c$b$a", True),  # Dollar signs
        ("100%", "%001", True),  # Percent and numbers
        ("a&b", "b&a", True),  # Ampersand
        ("a*b*c", "c*b*a", True),  # Asterisks
        ("(abc)", ")cba(", True),  # Parentheses
    ])
    def test_api_special_characters(self, client, input1, input2, expected):
        """Test API with special characters"""
        with allure.step(f"POST /api/check with special chars: '{input1}' and '{input2}'"):
            response = client.post(
                "/api/check",
                json={"input1": input1, "input2": input2}
            )

        with allure.step("Verify response handles special characters"):
            assert response.status_code == 200
            data = response.json()
            assert data["result"] == expected

        allure.attach(
            f"Input 1: {input1}\nInput 2: {input2}\nExpected: {expected}\nActual: {data['result']}",
            name="Special Characters Test",
            attachment_type=allure.attachment_type.TEXT
        )

    # ==================== Unicode Tests ====================
    
    @allure.title("Test API with Unicode characters")
    @pytest.mark.parametrize("input1,input2,expected", [
        ("café", "éfac", True),  # Accented characters
        ("naïve", "veïan", True),  # Diaeresis
        ("hello", "hëllo", False),  # Different unicode chars
        ("日本", "本日", True),  # Japanese characters
        ("Привет", "тевирП", True),  # Cyrillic
        ("🎉🎊", "🎊🎉", True),  # Emojis
        ("mañana", "añanam", True),  # Spanish ñ
        ("Zürich", "hcirüZ", True),  # German umlaut
    ])
    def test_api_unicode_characters(self, client, input1, input2, expected):
        """Test API with Unicode and international characters"""
        with allure.step(f"POST /api/check with Unicode: '{input1}' and '{input2}'"):
            response = client.post(
                "/api/check",
                json={"input1": input1, "input2": input2}
            )

        with allure.step("Verify response handles Unicode"):
            assert response.status_code == 200
            data = response.json()
            assert data["result"] == expected

        allure.attach(
            f"Input 1: {input1}\nInput 2: {input2}\nExpected: {expected}\nActual: {data['result']}",
            name="Unicode Test",
            attachment_type=allure.attachment_type.TEXT
        )

    # ==================== Whitespace Tests ====================
    
    @allure.title("Test API with whitespace variations")
    @pytest.mark.parametrize("input1,input2,expected", [
        ("a b c", "cba", True),  # Spaces removed
        ("  hello  ", "olleh", True),  # Leading/trailing spaces
        ("a\tb\tc", "cba", True),  # Tabs
        ("a\nb\nc", "cba", True),  # Newlines
        ("multiple   spaces", "spaces   multiple", True),  # Multiple spaces
        ("\thello\n", "olleh", True),  # Mixed whitespace
    ])
    def test_api_whitespace_variations(self, client, input1, input2, expected):
        """Test API with various whitespace scenarios"""
        with allure.step(f"POST /api/check with whitespace variations"):
            response = client.post(
                "/api/check",
                json={"input1": input1, "input2": input2}
            )

        with allure.step("Verify whitespace handling"):
            assert response.status_code == 200
            data = response.json()
            assert data["result"] == expected

        allure.attach(
            f"Input 1: {repr(input1)}\nInput 2: {repr(input2)}\nExpected: {expected}\nActual: {data['result']}",
            name="Whitespace Test",
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.title("Test API with only whitespace")
    def test_api_only_whitespace(self, client):
        """Test API with strings containing only whitespace"""
        with allure.step("POST /api/check with only spaces"):
            response = client.post(
                "/api/check",
                json={"input1": "   ", "input2": "   "}
            )

        with allure.step("Verify whitespace-only handling"):
            assert response.status_code == 200
            data = response.json()
            assert data["result"] == True

    # ==================== Numeric Tests ====================
    
    @allure.title("Test API with numeric strings")
    @pytest.mark.parametrize("input1,input2,expected", [
        ("123", "321", True),  # Pure numbers
        ("abc123", "321cba", True),  # Mixed alphanumeric
        ("1000", "0001", True),  # Leading zeros
        ("123", "124", False),  # Different numbers
        ("0", "0", True),  # Single zero
        ("999999999", "999999999", True),  # Large numbers
    ])
    def test_api_numeric_strings(self, client, input1, input2, expected):
        """Test API with numeric strings"""
        with allure.step(f"POST /api/check with numbers: '{input1}' and '{input2}'"):
            response = client.post(
                "/api/check",
                json={"input1": input1, "input2": input2}
            )

        with allure.step("Verify numeric string handling"):
            assert response.status_code == 200
            data = response.json()
            assert data["result"] == expected

    # ==================== Edge Case Tests ====================
    
    @allure.title("Test API with single character")
    @pytest.mark.parametrize("input1,input2,expected", [
        ("a", "a", True),  # Same single char
        ("a", "b", False),  # Different single char
        ("A", "a", True),  # Case insensitive single char
        ("1", "1", True),  # Single digit
        ("!", "!", True),  # Single special char
    ])
    def test_api_single_character(self, client, input1, input2, expected):
        """Test API with single character inputs"""
        with allure.step(f"POST /api/check with single chars: '{input1}' and '{input2}'"):
            response = client.post(
                "/api/check",
                json={"input1": input1, "input2": input2}
            )

        with allure.step("Verify single character handling"):
            assert response.status_code == 200
            data = response.json()
            assert data["result"] == expected

    @allure.title("Test API with very long strings (1K)")
    def test_api_long_strings_1k(self, client):
        """Test API with 1000 character strings"""
        long_str1 = "a" * 500 + "b" * 500
        long_str2 = "b" * 500 + "a" * 500

        with allure.step("POST /api/check with 1000 character strings"):
            response = client.post(
                "/api/check",
                json={"input1": long_str1, "input2": long_str2}
            )

        with allure.step("Verify long string handling"):
            assert response.status_code == 200
            data = response.json()
            assert data["result"] == True

        allure.attach(
            f"String length: {len(long_str1)} characters\nResult: {data['result']}",
            name="1K String Test",
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.title("Test API with very long strings (10K)")
    def test_api_very_long_strings_10k(self, client):
        """Test API with 10000 character strings"""
        very_long_str1 = "abc" * 3333 + "d"
        very_long_str2 = "d" + "cba" * 3333

        with allure.step("POST /api/check with 10K character strings"):
            response = client.post(
                "/api/check",
                json={"input1": very_long_str1, "input2": very_long_str2}
            )

        with allure.step("Verify very long string handling"):
            assert response.status_code == 200
            data = response.json()
            assert data["result"] == True

        allure.attach(
            f"String length: {len(very_long_str1)} characters\nResult: {data['result']}",
            name="10K String Test",
            attachment_type=allure.attachment_type.TEXT
        )

    @allure.title("Test API with null bytes")
    def test_api_null_bytes(self, client):
        """Test API with null bytes in strings"""
        with allure.step("POST /api/check with null bytes"):
            response = client.post(
                "/api/check",
                json={"input1": "hello\x00world", "input2": "world\x00hello"}
            )

        with allure.step("Verify null byte handling"):
            assert response.status_code == 200
            data = response.json()
            assert data["result"] == True

    @allure.title("Test API with wrong content type")
    def test_api_wrong_content_type(self, client):
        """Test API with wrong content type"""
        with allure.step("POST /api/check with form data instead of JSON"):
            response = client.post(
                "/api/check",
                data={"input1": "test", "input2": "test"}
            )

        with allure.step("Verify content type validation"):
            assert response.status_code == 422

    # ==================== Repeated Characters Tests ====================
    
    @allure.title("Test API with repeated characters")
    @pytest.mark.parametrize("input1,input2,expected", [
        ("aaa", "aaa", True),  # Same repeated chars
        ("aaa", "aab", False),  # Different count
        ("aaabbb", "bbbaaa", True),  # Multiple repeated chars
        ("aaaa", "aaaaa", False),  # Different length
        ("abcabc", "bcabca", True),  # Repeated patterns
        ("aaaaaaaaaa", "aaaaaaaaaa", True),  # Many repetitions
    ])
    def test_api_repeated_characters(self, client, input1, input2, expected):
        """Test API with repeated characters"""
        with allure.step(f"POST /api/check with repeated chars: '{input1}' and '{input2}'"):
            response = client.post(
                "/api/check",
                json={"input1": input1, "input2": input2}
            )

        with allure.step("Verify repeated character handling"):
            assert response.status_code == 200
            data = response.json()
            assert data["result"] == expected

    # ==================== Case Sensitivity Tests ====================
    
    @allure.title("Test API with case sensitivity")
    @pytest.mark.parametrize("input1,input2,expected", [
        ("ABC", "abc", True),  # All uppercase vs lowercase
        ("AbC", "CbA", True),  # Mixed case
        ("LISTEN", "silent", True),  # Different case anagrams
        ("HeLLo", "oLLeH", True),  # Random case mix
    ])
    def test_api_case_sensitivity(self, client, input1, input2, expected):
        """Test API case insensitivity"""
        with allure.step(f"POST /api/check with different cases: '{input1}' and '{input2}'"):
            response = client.post(
                "/api/check",
                json={"input1": input1, "input2": input2}
            )

        with allure.step("Verify case insensitive comparison"):
            assert response.status_code == 200
            data = response.json()
            assert data["result"] == expected

    # ==================== Mixed Content Tests ====================
    
    @allure.title("Test API with mixed alphanumeric")
    @pytest.mark.parametrize("input1,input2,expected", [
        ("abc123def", "fed321cba", True),
        ("Test1234", "4321tseT", True),
        ("a1b2c3", "3c2b1a", True),
        ("abc123", "abc124", False),
    ])
    def test_api_mixed_alphanumeric(self, client, input1, input2, expected):
        """Test API with mixed alphanumeric strings"""
        with allure.step(f"POST /api/check with mixed alphanumeric"):
            response = client.post(
                "/api/check",
                json={"input1": input1, "input2": input2}
            )

        with allure.step("Verify mixed content handling"):
            assert response.status_code == 200
            data = response.json()
            assert data["result"] == expected

    @allure.title("Test API performance with complex strings")
    def test_api_complex_performance(self, client):
        """Test API with complex mixed content"""
        complex_str1 = "The Quick! Brown@ Fox# Jumps$ Over% The^ Lazy& Dog* 123"
        complex_str2 = "*dog& yzaL^ ehT% revO$ spmuj# xoF@ nworB! kciuQ eht 321"
        
        with allure.step("POST /api/check with complex strings"):
            response = client.post(
                "/api/check",
                json={"input1": complex_str1, "input2": complex_str2}
            )

        with allure.step("Verify complex string handling"):
            assert response.status_code == 200
            data = response.json()
            assert data["result"] == True

    # ==================== BDD Style Tests ====================
    
    @allure.title("BDD: Check if two strings are anagrams via API")
    @pytest.mark.bdd
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
