# Fly.io Deployment Guide

This guide explains how to set up automatic deployment to Fly.io when merging from develop to main.

## Overview

The CI/CD pipeline includes automatic deployment to Fly.io that:
- ✅ Only triggers on merges to `main` branch
- ✅ Waits for all tests to pass
- ✅ Deploys using Docker container
- ✅ Verifies deployment health
- ✅ Provides deployment summary with links

## Prerequisites

1. **Fly.io Account**: Create account at https://fly.io/
2. **Fly.io CLI**: Install locally for initial setup
3. **GitHub Repository**: Your code pushed to GitHub

## Initial Setup

### Step 1: Install Fly.io CLI

**macOS/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

**Windows:**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

### Step 2: Login to Fly.io

```bash
flyctl auth login
```

This will open your browser for authentication.

### Step 3: Create Fly.io App (First Time Only)

If you haven't created the app yet:

```bash
# Launch the app (this uses the existing fly.toml)
flyctl launch --no-deploy

# Or if you want to create from scratch:
flyctl apps create anagram

# Set secrets if needed
flyctl secrets set SECRET_KEY=your-secret-key
```

The app is already configured in [fly.toml](fly.toml) with the name `anagram`.

### Step 4: Get Fly.io API Token

```bash
# Generate a new deploy token
flyctl tokens create deploy -x 999999h

# Or get your personal token
flyctl auth token
```

Copy the token output - you'll need it for GitHub.

### Step 5: Add Token to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `FLY_API_TOKEN`
5. Value: Paste the token from Step 4
6. Click **Add secret**

## How It Works

### Deployment Trigger

The deployment job runs when:
```yaml
if: |
  github.event_name == 'push' &&
  github.ref == 'refs/heads/main' &&
  (contains(github.event.head_commit.message, 'Merge') ||
   contains(github.event.head_commit.message, 'merge'))
```

This means deployment happens **only** when:
- ✅ It's a push to `main` branch
- ✅ The commit message contains "Merge" or "merge" (indicating a merge from develop)

### Deployment Workflow

```
┌─────────────────────────────────────────────────────┐
│  1. Developer merges develop → main                 │
└───────────────┬─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────┐
│  2. GitHub Actions CI/CD Pipeline Starts            │
│     - Unit Tests (parallel)                         │
│     - API Tests (parallel)                          │
│     - BDD Tests with 3 browsers (parallel)          │
└───────────────┬─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────┐
│  3. Aggregate & Report                              │
│     - Merge all test results                        │
│     - Generate Allure reports                       │
│     - Deploy to GitHub Pages                        │
└───────────────┬─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────┐
│  4. Deploy to Fly.io (if tests pass)                │
│     - Build Docker image                            │
│     - Deploy to Fly.io                              │
│     - Verify health endpoint                        │
│     - Create deployment summary                     │
└───────────────┬─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────┐
│  5. App Live at https://anagram.fly.dev             │
└─────────────────────────────────────────────────────┘
```

## Testing the Deployment

### Option 1: Merge from develop to main

```bash
# Create and switch to develop branch
git checkout -b develop
git push -u origin develop

# Make some changes
echo "# Update" >> README.md
git add .
git commit -m "Update README"
git push

# Merge to main
git checkout main
git merge develop
git push origin main
```

### Option 2: Create a Pull Request

1. Create a PR from `develop` to `main` on GitHub
2. Review and approve
3. Click "Merge pull request"
4. The deployment will automatically trigger

## Monitoring Deployment

### GitHub Actions

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. Click on the latest workflow run
4. Expand the **Deploy to Fly.io** job
5. View deployment logs and summary

### Deployment Summary

After deployment, GitHub will show a summary with:
- ✅ Deployment status
- 🌐 Application URL
- 📊 Fly.io dashboard link
- 📖 API documentation link
- Commit and branch details

### Fly.io Dashboard

Monitor your app at: https://fly.io/apps/anagram

View:
- Application status
- Logs: `flyctl logs -a anagram`
- Metrics
- Scaling configuration

## Application URLs

After successful deployment:

| Resource | URL |
|----------|-----|
| Application | https://anagram.fly.dev |
| Health Check | https://anagram.fly.dev/health |
| API Documentation | https://anagram.fly.dev/docs |
| Alternative API Docs | https://anagram.fly.dev/redoc |
| Fly.io Dashboard | https://fly.io/apps/anagram |

## Configuration Files

### fly.toml

The [fly.toml](fly.toml) file configures:
- App name: `anagram`
- Build: Uses Dockerfile
- Port: 8000 (internal), 80/443 (external)
- Auto-stop/start: Enabled (saves costs)

### Dockerfile

The [Dockerfile](Dockerfile) creates:
- Python 3.11 slim image
- Installs dependencies from requirements.txt
- Runs FastAPI with uvicorn
- Uses PORT environment variable from Fly.io

## Deployment Commands

### Manual Deployment

If you need to deploy manually:

```bash
# Deploy from local machine
flyctl deploy

# Deploy without local build (uses remote builder)
flyctl deploy --remote-only

# Deploy specific image
flyctl deploy --image registry.fly.io/anagram:latest
```

### Useful Fly.io Commands

```bash
# View app status
flyctl status -a anagram

# View logs
flyctl logs -a anagram

# Open app in browser
flyctl open -a anagram

# SSH into machine
flyctl ssh console -a anagram

# View secrets
flyctl secrets list -a anagram

# Set secret
flyctl secrets set KEY=value -a anagram

# Scale app
flyctl scale count 2 -a anagram

# Check deployment history
flyctl releases -a anagram

# Restart app
flyctl apps restart anagram
```

## Scaling

### Vertical Scaling (Machine Size)

```bash
# List available machine sizes
flyctl platform vm-sizes

# Scale to larger machine
flyctl scale vm shared-cpu-2x --memory 1024 -a anagram
```

### Horizontal Scaling (Multiple Instances)

```bash
# Scale to 2 instances
flyctl scale count 2 -a anagram

# Scale to specific regions
flyctl regions add sea syd -a anagram
flyctl scale count 3 -a anagram
```

### Auto-scaling

Modify `fly.toml`:
```toml
[[services]]
  min_machines_running = 1  # Keep at least 1 running
  auto_stop_machines = true
  auto_start_machines = true
```

## Environment Variables

Set environment variables (secrets):

```bash
# Set individual secret
flyctl secrets set SECRET_KEY=your-secret-key -a anagram

# Set multiple secrets
flyctl secrets set \
  SECRET_KEY=your-secret-key \
  DATABASE_URL=postgres://... \
  -a anagram

# Import from .env file
flyctl secrets import < .env -a anagram
```

## Troubleshooting

### Deployment Fails

**Check logs:**
```bash
flyctl logs -a anagram
```

**Common issues:**
- **Token expired**: Generate new token and update GitHub secret
- **Build error**: Check Dockerfile and dependencies
- **Port mismatch**: Ensure app uses `PORT` environment variable
- **Health check fails**: Verify `/health` endpoint works

### App Not Starting

```bash
# View detailed status
flyctl status -a anagram --all

# Check machine logs
flyctl logs -a anagram

# Restart app
flyctl apps restart anagram

# SSH into machine
flyctl ssh console -a anagram
```

### Slow Response Times

```bash
# Check metrics
flyctl metrics -a anagram

# Scale up machine size
flyctl scale vm shared-cpu-2x --memory 1024 -a anagram

# Add more instances
flyctl scale count 2 -a anagram
```

### Health Check Fails in CI/CD

The pipeline waits 5 minutes for health check. If it fails:
1. Check if `/health` endpoint exists in your FastAPI app
2. Verify the endpoint returns 200 status
3. Check Fly.io dashboard for app status
4. Review Fly.io logs for errors

## Cost Management

### Free Tier Limits

Fly.io free tier includes:
- Up to 3 shared-cpu-1x 256MB VMs
- 3GB persistent volume storage
- 160GB outbound data transfer

### Minimize Costs

```toml
# In fly.toml, enable auto-stop
[[services]]
  min_machines_running = 0  # Stop when idle
  auto_stop_machines = true
  auto_start_machines = true
```

```bash
# Stop app when not in use
flyctl apps stop anagram

# Start when needed
flyctl apps start anagram

# Destroy app (if no longer needed)
flyctl apps destroy anagram
```

## Security Best Practices

1. **Use deploy tokens** instead of personal tokens
2. **Rotate tokens regularly**
3. **Store secrets** in Fly.io secrets, not code
4. **Enable HTTPS** (automatic with Fly.io)
5. **Use environment-specific configs**
6. **Audit access logs** regularly

## CI/CD Integration Summary

The GitHub Actions workflow:

1. ✅ **Triggers**: Only on merge to main
2. ✅ **Dependencies**: Requires all tests to pass
3. ✅ **Build**: Uses Dockerfile for consistent builds
4. ✅ **Deploy**: Remote build on Fly.io infrastructure
5. ✅ **Verify**: Checks health endpoint after deployment
6. ✅ **Report**: Creates deployment summary in GitHub

## Additional Resources

- [Fly.io Documentation](https://fly.io/docs/)
- [Fly.io Python Guide](https://fly.io/docs/languages-and-frameworks/python/)
- [Fly.io Pricing](https://fly.io/docs/about/pricing/)
- [flyctl Command Reference](https://fly.io/docs/flyctl/)
- [Fly.io Status Page](https://status.flyio.net/)

## Support

If you need help:
1. Check [Fly.io Community](https://community.fly.io/)
2. Review [GitHub Actions logs](https://github.com/YOUR_USERNAME/smbc_test/actions)
3. Check application logs: `flyctl logs -a anagram`
4. Open issue in your repository
