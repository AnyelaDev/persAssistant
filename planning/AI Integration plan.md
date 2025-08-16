# AI/LLM Integration Architecture

This document defines the detailed architecture for AI/LLM integration in the Personal Assistant application, specifically for ToDo list grooming functionality.

## Architecture Overview

The AI integration follows a modular approach with clear separation of concerns:
- **Prompt Management**: Structured prompt templates
- **API Layer**: Configurable service providers with fallback mechanisms
- **Processing Layer**: Response parsing and validation
- **Integration Layer**: Seamless UI integration with error handling

## Prompt Templates for ToDo Grooming

### Base Prompt Template
```python
GROOMING_PROMPT_TEMPLATE = """
You are an AI assistant specialized in organizing and optimizing todo lists. Your task is to improve the given todo list by:

1. Clarifying vague or unclear tasks
2. Breaking down large tasks into smaller, actionable items
3. Removing duplicates and consolidating similar items
4. Improving task descriptions for clarity
5. Suggesting logical priority ordering

Input Todo List:
{todo_list}

Please respond with a JSON object containing:
{
    "groomed_tasks": [
        {
            "title": "Clear, actionable task description",
            "estimated_time": "HH:MM format (optional)",
            "priority": "high|medium|low",
            "notes": "Any clarification or context"
            "source":"Textual reference to the original input that relates to this task"
        }
    ],
    "suggestions": ["Any general recommendations"],
    "removed_items": ["Duplicate or unnecessary items removed"],
    "processing_notes": "Brief summary of changes made"
}

Ensure all tasks are:
- Specific and actionable
- Clearly worded
- Appropriately sized (can be completed in reasonable time)
- Free of duplicates
- Alert of any logic inconsistency
"""

PROMPT_VERSION = "1.0"
```

### Specialized Prompt Variants
```python
# For very long todo lists (>10 items)
LONG_LIST_PROMPT_TEMPLATE = """
{base_template}

Special instructions for large lists:
- Group related tasks into categories
- Identify and separate urgent vs non-urgent items
- Suggest task batching opportunities
"""

# For todo lists with dependencies
DEPENDENCY_AWARE_PROMPT_TEMPLATE = """
{base_template}

Additional requirements:
- Identify task dependencies and ordering requirements
- Suggest parallel vs sequential execution paths
- Flag tasks that block other tasks
"""
```

## API Handling Strategy

### Service Provider Options

#### Primary: Hugging Face Inference API
```python
# Configuration
HF_CONFIG = {
    "base_url": "https://api-inference.huggingface.co/models/",
    "model": "mistralai/Mistral-7B-Instruct-v0.2",
    "timeout": 30,
    "max_retries": 2,
    "retry_delay": 2
}
```

#### Alternative: OpenAI API (for premium features)
```python
OPENAI_CONFIG = {
    "model": "gpt-3.5-turbo",
    "max_tokens": 2000,
    "temperature": 0.3
}
```

#### Local Inference Option (future)
```python
LOCAL_CONFIG = {
    "model_path": "./models/local-grooming-model",
    "inference_engine": "ollama",
    "fallback_enabled": True
}
```

### Service Selection Logic
```python
def get_active_service():
    """
    Returns active AI service based on configuration and availability
    Priority: Local -> OpenAI -> Hugging Face -> Fallback
    """
    if config.LOCAL_AI_ENABLED and local_service.is_available():
        return "local"
    elif config.OPENAI_API_KEY and openai_service.test_connection():
        return "openai"  
    elif config.HF_API_KEY:
        return "huggingface"
    else:
        return "fallback"
```

## Error Fallback Mechanisms

### Fallback Hierarchy
1. **Primary Service Failure** → Retry with exponential backoff
2. **Repeated Failures** → Switch to secondary service
3. **All Services Down** → Graceful degradation with basic grooming
4. **Network Issues** → Offline mode with cached suggestions

### Fallback Implementation
```python
class GroomingService:
    def groom_list(self, todo_list):
        for service in self.service_priority:
            try:
                result = self._attempt_grooming(service, todo_list)
                if result.is_valid():
                    return result
            except ServiceUnavailableError:
                continue
            except APIQuotaExceededError:
                self._switch_to_fallback_service()
                continue
        
        # Final fallback: basic rule-based grooming
        return self._basic_grooming_fallback(todo_list)
    
    def _basic_grooming_fallback(self, todo_list):
        """Basic grooming without AI: numbering, deduplication, basic formatting"""
        return BasicGroomer().process(todo_list)
```

### Error User Experience
- **Loading States**: Show progress indicator during API calls
- **Error Messages**: User-friendly explanations ("AI service temporarily unavailable")
- **Degraded Mode**: Continue with basic grooming functionality
- **Recovery**: Automatic retry when service becomes available

## Model Selection Criteria and Configuration

### Selection Criteria
```python
MODEL_SELECTION_CRITERIA = {
    "response_time": "< 10 seconds preferred",
    "accuracy": "90%+ valid JSON responses", 
    "cost": "Free tier available for basic usage",
    "reliability": "99%+ uptime",
    "context_length": "4K+ tokens for large todo lists",
    "language_support": "English (primary), multilingual preferred"
}
```

### Configuration Management
```python
# config/ai_settings.py
class AIConfig:
    def __init__(self):
        self.primary_service = os.getenv("AI_PRIMARY_SERVICE", "huggingface")
        self.fallback_enabled = os.getenv("AI_FALLBACK_ENABLED", "true").lower() == "true"
        self.timeout = int(os.getenv("AI_TIMEOUT", "30"))
        self.max_retries = int(os.getenv("AI_MAX_RETRIES", "2"))
        self.cache_responses = os.getenv("AI_CACHE_ENABLED", "true").lower() == "true"
```

### Model Performance Tracking
```python
# Automatic model evaluation and switching
class ModelPerformanceTracker:
    def track_request(self, model, success, response_time, parse_success):
        """Track model performance metrics"""
        
    def should_switch_model(self):
        """Determine if model switching is recommended based on performance"""
        
    def get_recommended_model(self):
        """Return best performing model based on recent metrics"""
```

## API Key Management and Security

### Security Best Practices
```python
# Environment-based configuration
API_KEYS = {
    "huggingface": os.getenv("HF_API_KEY"),
    "openai": os.getenv("OPENAI_API_KEY"),
    "claude": os.getenv("ANTHROPIC_API_KEY")
}

# Key validation
def validate_api_keys():
    """Validate API keys on startup without exposing them in logs"""
    for service, key in API_KEYS.items():
        if key and not _test_key_format(service, key):
            logger.warning(f"Invalid {service} API key format")
```

### Key Management Features
- **Environment Variables**: Never commit keys to repository
- **Key Rotation**: Support for updating keys without app restart
- **Validation**: Test key validity on startup
- **Logging**: Never log actual key values
- **Encryption**: Encrypt keys in local storage (future enhancement)

### Configuration UI
```python
# Settings screen for API key management
class AISettingsScreen:
    def configure_api_keys(self):
        """Secure UI for API key configuration"""
        # Masked input fields
        # Key validation feedback
        # Service availability testing
```

## Integration Testing Strategy

### Test Categories

#### 1. Unit Tests
```python
# tests/test_ai/test_grooming_service.py
def test_prompt_template_formatting():
    """Test prompt template with various input formats"""

def test_response_parsing():
    """Test JSON response parsing and validation"""

def test_error_handling():
    """Test various error scenarios and fallbacks"""
```

#### 2. Integration Tests
```python
# tests/test_ai/test_api_integration.py
def test_huggingface_api_call():
    """Test actual API call to Hugging Face (with mocking for CI)"""

def test_service_switching():
    """Test automatic switching between services"""

def test_fallback_mechanisms():
    """Test graceful degradation when services fail"""
```

#### 3. Mock Testing Strategy
```python
# Use responses library for HTTP mocking
@responses.activate
def test_api_timeout_handling():
    responses.add(
        responses.POST,
        "https://api-inference.huggingface.co/models/...",
        json={"error": "timeout"},
        status=408
    )
    # Test timeout handling
```

#### 4. Golden Set Testing
```python
# Predefined test cases for consistency
GOLDEN_SET_TESTS = [
    {
        "input": "grocery shopping, buy milk, get bread, pick up groceries",
        "expected_deduplication": True,
        "expected_task_count": 2
    },
    {
        "input": "plan vacation, book flights, book hotel, pack bags",
        "expected_dependency_detection": True,
        "expected_ordering": ["plan vacation", "book flights", "book hotel", "pack bags"]
    }
]
```

### Test Automation
```python
# CI/CD pipeline integration
def run_ai_integration_tests():
    """Automated testing in CI pipeline"""
    if os.getenv("CI_MODE"):
        # Use mocked responses in CI
        run_mocked_tests()
    else:
        # Use real API calls in development
        run_live_api_tests()
```

## **📋 Phase 1 — First End-to-End Call (Week 1)**

Goal: Click button → send text to Hugging Face → show raw response in UI.

1. **Hugging Face Setup**

   * [ ] Create a free account on Hugging Face.
   * [ ] Go to profile → Settings → Access Tokens → create new token.
   * [ ] Store token in `.env` file:

     ```
     HF_API_KEY=xxxxxxxxxxxxxxxx
     ```
   * [ ] Install `python-dotenv` (`pip install python-dotenv`) to load the key.

2. **API Test in Python**

   * [ ] Create `api_test.py`.
   * [ ] Write a request to any text model (e.g., `mistralai/Mistral-7B-Instruct-v0.2`) using `requests`.
   * [ ] Run and print the raw JSON result in console.

3. **Integrate with App UI**

   * [ ] Create a function `get_model_response(prompt)` in a `ai/grooming_service.py` file.
   * [ ] Connect the "Groom my list" button in the UI to call this function with the user's input.
   * [ ] Display the raw JSON response text in the UI (no formatting yet).

**✅ Definition of Done:** You can click a button in the app and see the Hugging Face model's raw output in the UI.

---

## **📋 Phase 2 — Structured Output & Error Handling (Week 2–3)**

Goal: Model returns structured data, app parses and displays it correctly.

4. **Prompt Update**

   * [ ] Change prompt to include “Respond in JSON with keys: task\_list, notes”.
   * [ ] Test in console until output is mostly valid JSON.

5. **Parsing Layer**

   * [ ] Write `parse_model_output(raw_output)` function:

     * If valid JSON → return dict.
     * If invalid → return empty dict or fallback text.

6. **Error Handling**

   * [ ] Wrap API call in `try/except`.
   * [ ] Retry **once** if it fails (sleep 2 seconds between tries).
   * [ ] If it still fails → return message `"Model not available"`.

7. **UI Display**

   * [ ] Take parsed `task_list` and render as bullet points.
   * [ ] Show `notes` in a separate box.

**✅ Definition of Done:** 80% of runs show correctly formatted tasks in the UI without crashes.

---

## **📋 Phase 3 — Quality Pass & Simple Logging (Week 4)**

Goal: Responses are stable and success rate is tracked.

8. **Golden Set Creation**

   * [ ] Pick 5–10 real prompts from the product use case.
   * [ ] Save them in `golden_set.json`.

9. **Manual Evaluation**

   * [ ] Run each golden set prompt 3 times.
   * [ ] Note when parsing fails or the content is wrong.

10. **Prompt Tuning**

    * [ ] Modify prompt wording to improve output.
    * [ ] Keep a `PROMPT_VERSION` variable at the top of `prompts.py`.

11. **Logging**

    * [ ] Create a `logs.csv` file with headers:

      ```
      timestamp,prompt_version,model_name,success
      ```
    * [ ] Append one line per request, with 1 or 0 in `success`.

12. **Final Demo Prep**

    * [ ] Run app with golden set prompts.
    * [ ] Show that UI displays structured tasks and success rate in logs is ≥90%.

**✅ Definition of Done:** Stable results, reproducible with the golden set, and logging in place.

---