# Configuration Architecture Explained

**Date:** December 2, 2025

## Question: Why is there duplication between `src/config.py` and `.env`?

**Short Answer:** It's not duplication - it's a **fallback pattern**. The `.env` file is **optional** and only used for local overrides. The app works without it.

## How It Works

### Configuration Priority (Highest to Lowest)

1. **Environment Variables** (exported in shell/system)
2. **`.env` File** (local customization)
3. **`src/config.py` Defaults** (fallback values)

```python
# src/config.py - Provides defaults
class Settings(BaseSettings):
    port: int = 8000  # ← Default value

# .env file - Optional override
PORT=3000  # ← Override default

# Environment variable - Highest priority
export PORT=9000  # ← Wins over everything
```

### Real Example

```bash
# 1. No .env file, no env vars → Uses config.py defaults
$ rm .env
$ python -c "from src.config import settings; print(settings.port)"
8000  # From config.py default

# 2. With .env file → Uses .env value
$ echo "PORT=3000" > .env
$ python -c "from src.config import settings; print(settings.port)"
3000  # From .env file

# 3. With environment variable → Uses env var (highest priority)
$ export PORT=9000
$ python -c "from src.config import settings; print(settings.port)"
9000  # From environment variable
```

## Why This Design?

### ✅ Benefits of Current Architecture

1. **App Works Out-of-the-Box**
   - No `.env` file needed
   - Sensible defaults built-in
   - Quick start for new developers

2. **Environment Flexibility**
   - **Development:** Use `.env` for custom colors, ports, etc.
   - **CI/CD:** GitHub Actions sets env vars directly
   - **Production:** Fly.io/Docker uses env vars
   - **Testing:** Tests can override specific settings

3. **Self-Documenting Code**
   - Type hints in `config.py` show what's available
   - Default values show recommended settings
   - Pydantic validates all values

4. **Security**
   - `.env` never committed to git
   - Production uses platform-specific env vars
   - No secrets in code

5. **12-Factor App Compliance**
   - Configuration separated from code
   - Environment-specific config
   - Easy deployment to any platform

### ❌ If `.env` Was the Only Source

If we removed defaults from `config.py`:

```python
# BAD: No defaults
class Settings(BaseSettings):
    port: int  # ← Required, no default
```

**Problems:**
- ❌ App crashes without `.env` file
- ❌ Must create `.env` before first run
- ❌ No documentation of available settings
- ❌ Type hints disconnected from defaults
- ❌ Can't run in environments without files (Docker, Lambda, etc.)

## File Purposes

### `src/config.py` (Code Defaults)

**Purpose:**
- Provides fallback defaults
- Type definitions and validation
- Documentation of all settings
- Works in any environment

**Who uses it:**
- All environments (dev, test, prod)
- Always loaded
- Single source of truth for **what settings exist**

```python
# Example: src/config.py
class Settings(BaseSettings):
    # These are defaults - the app works with these values
    app_name: str = "Anagram Checker API"
    port: int = 8000
    ui_primary_color: str = "#4CAF50"
```

### `.env` File (Local Customization)

**Purpose:**
- **Optional** local overrides
- Developer-specific preferences
- Testing different configurations

**Who uses it:**
- **Local development only**
- **Not committed to git**
- **Not used in production**

```bash
# Example: .env (optional)
# Only customize what you want to change
UI_PRIMARY_COLOR=#FF5722  # Custom brand color
PORT=3000                  # Different port
# Everything else uses config.py defaults
```

### `.env.example` (Documentation)

**Purpose:**
- Shows all available options
- Template for creating `.env`
- Documentation with comments

**Who uses it:**
- New developers copying to `.env`
- Reference for what can be configured
- **Never loaded by the app**

## Common Use Cases

### 1. New Developer Setup

```bash
# Clone repo
git clone ...
cd SMBC

# Install dependencies
pip install -r requirements.txt

# Run immediately - works with defaults!
uvicorn src.app:app

# Optionally customize
cp .env.example .env
# Edit .env to change colors, port, etc.
```

### 2. Production Deployment (Fly.io)

```bash
# No .env file at all!
# Set secrets via platform
fly secrets set \
  ENVIRONMENT=production \
  DEBUG=false \
  CORS_ORIGINS=https://myapp.fly.dev \
  UI_PRIMARY_COLOR=#FF5722

# config.py provides all other defaults
```

### 3. CI/CD (GitHub Actions)

```yaml
# .github/workflows/ci.yml
env:
  # Only override what's different in CI
  ENVIRONMENT: testing
  DEBUG: false
  # config.py provides all other defaults
```

### 4. Docker

```dockerfile
# Dockerfile
ENV ENVIRONMENT=production
ENV HOST=0.0.0.0
ENV PORT=8000
# config.py provides all other defaults
```

## Configuration Loading Flow

```
┌─────────────────────────────────────────────────┐
│ 1. Pydantic Settings loads config.py defaults  │
│    port: int = 8000                             │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│ 2. Check for .env file (optional)              │
│    If exists: PORT=3000 → Overrides default    │
│    If missing: Keep default                    │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│ 3. Check environment variables (highest)       │
│    If exists: export PORT=9000 → Wins          │
│    If missing: Keep previous value             │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│ Final Result: port = 9000 (from env var)       │
└─────────────────────────────────────────────────┘
```

## Testing the Architecture

### Test 1: App Works Without .env

```bash
$ rm .env  # Remove .env file
$ python -c "from src.config import settings; print(settings.port)"
8000  # ✅ Works! Uses config.py default
```

### Test 2: .env Overrides Defaults

```bash
$ echo "PORT=3000" > .env
$ python -c "from src.config import settings; print(settings.port)"
3000  # ✅ Uses .env value
```

### Test 3: Environment Variable Wins

```bash
$ export PORT=9000
$ python -c "from src.config import settings; print(settings.port)"
9000  # ✅ Env var has highest priority
```

## Best Practices

### ✅ DO

1. **Keep defaults in `config.py`** for all settings
2. **Use `.env` only for local customization**
3. **Use environment variables in production**
4. **Keep `.env.example` updated** with all available options
5. **Document new settings** with comments

### ❌ DON'T

1. **Don't commit `.env`** to git (already in `.gitignore`)
2. **Don't require `.env`** - app must work without it
3. **Don't put secrets in code** - use env vars
4. **Don't duplicate logic** - one source of truth in `config.py`

## Summary

The "duplication" between `src/config.py` and `.env` is actually a **fallback pattern**:

- **`config.py`** = Defaults that work everywhere
- **`.env`** = Optional local overrides
- **Environment variables** = Production configuration

This design is:
- ✅ **Flexible** - Works in any environment
- ✅ **Secure** - Secrets in env vars, not files
- ✅ **Developer-friendly** - Works out-of-the-box
- ✅ **Production-ready** - Platform-agnostic
- ✅ **12-Factor compliant** - Industry best practice

**The `.env` file is NOT required - it's a convenience for local development.**

---

**References:**
- [12-Factor App: Config](https://12factor.net/config)
- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [docs/CONFIGURATION.md](CONFIGURATION.md) - Full configuration guide
