# Configuration Guide

## Environment Variables

The application uses environment variables for configuration management, making it easy to configure different environments (development, testing, production) without code changes.

## Configuration Files

### `.env` (Local Development)
Main configuration file for local development. This file contains all environment-specific settings.

**Location:** `/Users/sergei/Projects/SMBC/.env`

**⚠️ Security:** This file is excluded from git (listed in `.gitignore`) to prevent exposing sensitive configuration.

### `.env.example` (Template)
Template file showing all available configuration options. Copy this to create your own `.env` file.

**Location:** `/Users/sergei/Projects/SMBC/.env.example`

## Available Configuration Options

### Application Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | "Anagram Checker API" | Application name displayed in API docs |
| `APP_VERSION` | "1.0.0" | API version number |
| `APP_DESCRIPTION` | "API to check if two strings are anagrams" | API description |

### Server Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | "0.0.0.0" | Server host address |
| `PORT` | 8000 | Server port number |
| `RELOAD` | true | Enable auto-reload on code changes |

### API Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `API_PREFIX` | "/api" | API route prefix |
| `API_CHECK_ENDPOINT` | "/api/check" | Anagram check endpoint path |
| `HEALTH_ENDPOINT` | "/health" | Health check endpoint path |

### CORS Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `CORS_ORIGINS` | "*" | Allowed CORS origins (comma-separated or *) |
| `CORS_ALLOW_CREDENTIALS` | true | Allow credentials in CORS |
| `CORS_ALLOW_METHODS` | "*" | Allowed HTTP methods |
| `CORS_ALLOW_HEADERS` | "*" | Allowed HTTP headers |

### Application URLs

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | "http://localhost:8000" | Base URL for the application |
| `API_URL` | "http://localhost:8000/api" | API base URL |

### UI Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `UI_TITLE` | "Anagram Checker" | Web UI page title |
| `UI_PRIMARY_COLOR` | "#4CAF50" | Primary button color (hex) |
| `UI_PRIMARY_COLOR_HOVER` | "#45a049" | Button hover color (hex) |
| `COPYRIGHT_NAME` | "Siarhei Staravoitau" | Copyright holder name |

### Testing Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `TEST_SERVER_URL` | "http://localhost:8000" | Server URL for tests |
| `TEST_TIMEOUT` | 30000 | Test timeout in milliseconds |
| `TEST_BROWSER` | "firefox" | Browser for UI tests (firefox/chromium/webkit) |
| `TEST_HEADED` | false | Run browser in headed mode |

### Validation Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `MIN_INPUT_LENGTH` | 1 | Minimum string length |
| `MAX_INPUT_LENGTH` | 1000000 | Maximum string length (1M chars) |

### Environment Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | "development" | Environment name (development/testing/production) |
| `DEBUG` | true | Enable debug mode |

## Setup Instructions

### 1. Create Configuration File

```bash
# Copy the example file
cp .env.example .env

# Edit with your settings
nano .env  # or your preferred editor
```

### 2. Install Dependencies

```bash
pip install python-dotenv==1.0.0 pydantic-settings==2.1.0
```

### 3. Verify Configuration

```bash
python -c "from src.config import settings; print(settings.app_name)"
```

## Usage in Code

### Importing Settings

```python
from src.config import settings

# Access configuration
app_name = settings.app_name
port = settings.port
base_url = settings.base_url
```

### Using in FastAPI

```python
from fastapi import FastAPI
from src.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)

@app.get(settings.health_endpoint)
async def health():
    return {"status": "healthy"}
```

### Using in Tests

```python
import os
from dotenv import load_dotenv

load_dotenv()

TEST_SERVER_URL = os.getenv("TEST_SERVER_URL", "http://localhost:8000")
```

## Environment-Specific Configuration

### Development

```bash
# .env
ENVIRONMENT=development
DEBUG=true
HOST=0.0.0.0
PORT=8000
RELOAD=true
```

### Testing

```bash
# .env.test
ENVIRONMENT=testing
DEBUG=true
HOST=localhost
PORT=8001
RELOAD=false
TEST_HEADED=true
```

### Production

```bash
# .env.production
ENVIRONMENT=production
DEBUG=false
HOST=0.0.0.0
PORT=8000
RELOAD=false
CORS_ORIGINS=https://yourdomain.com
MAX_INPUT_LENGTH=100000
```

## Loading Different Environments

### Using specific env file

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.production"  # Specify file
    )
```

### Using environment variable

```bash
# Set environment first
export ENV_FILE=".env.production"

# Then load in code
import os
from dotenv import load_dotenv

env_file = os.getenv("ENV_FILE", ".env")
load_dotenv(env_file)
```

## Configuration Priority

Configuration values are loaded in this order (highest priority first):

1. **Environment variables** (set in shell/system)
2. **.env file** (local configuration file)
3. **Default values** (hardcoded in `src/config.py`)

Example:
```bash
# .env file has: PORT=8000
# Shell environment has: export PORT=9000
# Result: PORT=9000 (environment variable wins)
```

## Security Best Practices

### ✅ DO

- Keep `.env` in `.gitignore`
- Use `.env.example` for documentation
- Use strong, unique values in production
- Restrict CORS origins in production
- Set appropriate max input lengths
- Use environment variables for secrets
- Rotate secrets regularly

### ❌ DON'T

- Commit `.env` to git
- Use default values in production
- Share `.env` files via email/chat
- Store secrets in code
- Use `CORS_ORIGINS=*` in production
- Disable validation in production

## Troubleshooting

### Configuration Not Loading

```bash
# Check if .env file exists
ls -la .env

# Check file contents
cat .env

# Test loading
python -c "from src.config import settings; print(vars(settings))"
```

### Wrong Values Being Used

```bash
# Check environment variables
env | grep -E "APP_|PORT|HOST"

# Clear environment and reload
unset PORT
python -c "from src.config import settings; print(settings.port)"
```

### Module Not Found

```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import pydantic_settings; import dotenv"
```

## Examples

### Custom Configuration for CI/CD

```yaml
# .github/workflows/ci.yml
env:
  ENVIRONMENT: testing
  PORT: 8000
  TEST_SERVER_URL: http://localhost:8000
  DEBUG: false
```

### Docker Configuration

```dockerfile
# Dockerfile
ENV APP_NAME="Anagram Checker API"
ENV PORT=8000
ENV HOST=0.0.0.0
ENV ENVIRONMENT=production
```

### Fly.io Configuration

```toml
# fly.toml
[env]
  ENVIRONMENT = "production"
  PORT = "8080"
  DEBUG = "false"
```

## Configuration Schema

The configuration is validated using Pydantic, providing:

- **Type checking** - Ensures correct data types
- **Validation** - Checks value constraints
- **Auto-conversion** - Converts strings to appropriate types
- **Default values** - Provides sensible defaults
- **Documentation** - Self-documenting with type hints

## Related Files

- [src/config.py](../src/config.py) - Configuration module
- [.env.example](../.env.example) - Configuration template
- [.env](../.env) - Local configuration (not in git)
- [.gitignore](../.gitignore) - Git exclusions

## Support

For configuration issues:
1. Check this documentation
2. Review `.env.example` for correct format
3. Verify all required dependencies are installed
4. Check Python version compatibility (3.9+)

---

**Last Updated:** December 2025
**Author:** Project Team
