"""
FastAPI application for Anagram Checker
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from src.anagram_checker import create_anagram_checker
from src.models import AnagramRequest, AnagramResponse

app = FastAPI(
    title="Anagram Checker API",
    description="API to check if two strings are anagrams",
    version="1.0.0"
)

# CORS middleware for web UI access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create anagram checker instance
checker = create_anagram_checker()


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the web UI"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Anagram Checker</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
            }
            .form-group {
                margin: 20px 0;
            }
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
                color: #555;
            }
            input[type="text"] {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
                box-sizing: border-box;
            }
            button {
                width: 100%;
                padding: 12px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                margin-top: 10px;
            }
            button:hover {
                background-color: #45a049;
            }
            #result {
                margin-top: 20px;
                padding: 15px;
                border-radius: 5px;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
                display: none;
            }
            .result-true {
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .result-false {
                background-color: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            .example {
                background-color: #e7f3ff;
                padding: 15px;
                border-radius: 5px;
                margin-top: 20px;
            }
            .example h3 {
                margin-top: 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Anagram Checker</h1>
            <p style="text-align: center; color: #666;">
                Check if two strings are anagrams of each other
            </p>

            <form id="anagramForm">
                <div class="form-group">
                    <label for="input1">Input 1:</label>
                    <input type="text" id="input1" name="input1" required
                           placeholder="Enter first string" data-testid="input1">
                </div>

                <div class="form-group">
                    <label for="input2">Input 2:</label>
                    <input type="text" id="input2" name="input2" required
                           placeholder="Enter second string" data-testid="input2">
                </div>

                <button type="submit" data-testid="check-button">Check Anagram</button>
            </form>

            <div id="result" data-testid="result"></div>

            <div class="example">
                <h3>Examples:</h3>
                <ul>
                    <li><strong>listen</strong> and <strong>silent</strong> → TRUE</li>
                    <li><strong>hello</strong> and <strong>world</strong> → FALSE</li>
                    <li><strong>A gentleman</strong> and <strong>Elegant Man</strong> → TRUE</li>
                    <li><strong>school master</strong> and <strong>the classroom</strong> → TRUE</li>
                </ul>
            </div>

            <footer style="text-align: center; color: #777; margin-top: 25px; font-size: 14px;">
                <span id="copyright"></span>
            </footer>
        </div>

        <script>
            // Set current year in footer
            document.getElementById('copyright').textContent =
              `\u00A9 ${new Date().getFullYear()} Siarhei Staravoitau`;

            document.getElementById('anagramForm').addEventListener('submit', async (e) => {
                e.preventDefault();

                const input1 = document.getElementById('input1').value;
                const input2 = document.getElementById('input2').value;

                try {
                    const response = await fetch('/api/check', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ input1, input2 })
                    });

                    const data = await response.json();
                    const resultDiv = document.getElementById('result');

                    resultDiv.textContent = data.result ? 'TRUE - These are anagrams!' : 'FALSE - These are not anagrams';
                    resultDiv.className = data.result ? 'result-true' : 'result-false';
                    resultDiv.style.display = 'block';
                } catch (error) {
                    alert('Error checking anagram: ' + error.message);
                }
            });
        </script>
    </body>
    </html>
    """


@app.post("/api/check", response_model=AnagramResponse)
async def check_anagram(request: AnagramRequest):
    """
    Check if two strings are anagrams

    Args:
        request: AnagramRequest with input1 and input2

    Returns:
        AnagramResponse with the result
    """
    try:
        result = checker.check(request.input1, request.input2)
        return AnagramResponse(
            input1=request.input1,
            input2=request.input2,
            result=result
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
