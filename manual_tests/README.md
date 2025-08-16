# Manual Tests

This folder contains manual test scripts for debugging and testing specific functionality outside of the automated test suite.

## Files

### `test_huggingface_api.py`
**Purpose**: Test HuggingFace API integration manually to debug AI grooming issues.

**What it does**:
1. ✅ Loads your API key from `.env` file
2. ✅ Tests if your HuggingFace API key is valid
3. ✅ Tries multiple AI models to find one that works
4. ✅ Shows actual API responses and errors
5. ✅ Tests our GroomingService implementation
6. ✅ Provides recommendations for fixing issues

**How to run**:
```bash
# Make sure you have a valid HuggingFace API key in your .env file
python manual_tests/test_huggingface_api.py
```

**Expected output**:
- If API key is valid: Shows which models work and test results
- If API key is invalid: Shows clear error message and next steps
- If models are loading: Explains the 503 status and suggests waiting

**Troubleshooting**:
- **401 Unauthorized**: Your API key is invalid or expired
- **404 Not Found**: The model doesn't exist or isn't available
- **503 Service Unavailable**: Model is loading (normal for cold starts)
- **ImportError**: Make sure you're in the project root directory

## Usage

These manual tests are designed to help you:

1. **Debug API issues** without running the full application
2. **Test different API keys** quickly
3. **Find working AI models** when the default ones fail
4. **Understand API responses** in detail
5. **Verify the complete AI pipeline** step by step

Run these tests whenever:
- AI grooming isn't working as expected
- You get a new HuggingFace API key
- You want to try different AI models
- You're troubleshooting API connectivity issues