# Testing Guide

This directory contains the comprehensive test suite for the Personal Assistant application, organized using TDD best practices with a structured directory layout.

## Quick Start

Run core functionality tests (recommended for development):
```bash
python run_tests.py core
```

## Test Structure

The tests are organized in a **mirror structure** that follows the src/ directory layout:

```
tests/
├── test_core/           # Tests for src/core/
│   ├── test_models.py   # Tests for Task and TaskManager classes
│   └── test_timeline.py # Tests for timeline generation functionality
├── test_ui/             # Tests for src/ui/
│   ├── test_navigation.py      # Tests for screen navigation
│   └── test_ui_components.py   # Tests for UI component behavior
├── test_utils/          # Tests for src/utils/ (future use)
├── fixtures/            # Test data and app instance creators
│   └── app_fixtures.py  # Fixtures for real app components
├── helpers/             # Test utility functions
│   └── test_helpers.py  # Helper functions for user interaction simulation
├── e2e/                 # End-to-end user scenario tests (planned)
├── integration/         # Legacy integration tests (will be reorganized)
└── unit/                # Legacy unit test directory (will be reorganized)
```

### Core Files
- `conftest.py` - Pytest configuration and shared fixtures
- `fixtures/app_fixtures.py` - Real app instances and test data
- `helpers/test_helpers.py` - User interaction simulation helpers

## Running Tests

### Using the Test Runner Script (Recommended)

```bash
# Core functionality tests (models + timeline)
python run_tests.py core

# All model tests with coverage
python run_tests.py models

# All timeline tests
python run_tests.py timeline

# UI and navigation tests
python run_tests.py ui

# All tests in core module
python run_tests.py test_core

# All tests in UI module
python run_tests.py test_ui

# Unit tests (business logic only)
python run_tests.py unit

# Integration tests (UI interactions)
python run_tests.py integration

# Quick test (models only, minimal output)
python run_tests.py quick

# All tests (includes UI tests with known issues)
python run_tests.py all

# Save test output to log file
python run_tests.py core --save-log
```

### Test Categories

- **`core`** - Core business logic (models + timeline)
- **`models`** - Task and TaskManager classes only
- **`timeline`** - Timeline generation functionality
- **`ui`** - User interface and navigation tests
- **`test_core`** - All tests in test_core/ directory
- **`test_ui`** - All tests in test_ui/ directory  
- **`unit`** - Pure business logic tests
- **`integration`** - UI interaction tests
- **`quick`** - Fast test run for development

### Test Output Logging

All test configurations support `--save-log` flag to capture complete test output:

```bash
python run_tests.py models --save-log
# Saves to: logs/test_log_YYYYMMDD_HHMMSS_models.txt
```

Log files include:
- Complete test output (stdout/stderr)
- Timestamp and test type metadata
- Exit code and execution summary

### Using pytest directly

```bash
# Run all tests
pytest

# Run with coverage for specific module
pytest --cov=src.core

# Run specific test directory
pytest tests/test_core/

# Run specific test file
pytest tests/test_core/test_models.py

# Run with verbose output
pytest -v

# Run with coverage and HTML report
pytest --cov=src --cov-report=html
```

## Test Coverage

Current coverage for core functionality: **100%** for models.py

The core models (`Task` and `TaskManager`) have comprehensive test coverage including:
- Task creation and property management
- Dependency relationships and validation
- Task lifecycle (start, complete)
- TaskManager operations (add, remove, query)
- Timeline data generation
- Edge cases and error conditions

## Test Results Summary

✅ **30/30 model tests pass** - Core functionality fully tested  
✅ **9/10 timeline tests pass** - Timeline generation nearly complete (1 known bug)  
⚠️ **UI/Navigation tests** - Multiple failures due to over-mocking (being refactored)

### Known Issues

1. **Timeline Logic Bug**: Current task appears in both current_task and ready_tasks
2. **UI Test Over-Mocking**: Tests mock too many internal components, making them brittle
3. **Mock Configuration Issues**: Some tests attempt to set unsupported magic methods

## Testing Philosophy

This test suite is being migrated toward **better TDD practices**:

### Current State (Legacy)
- ❌ Over-mocking of internal components
- ❌ Testing implementation details vs. behavior
- ❌ Brittle tests that break during refactoring

### Target State (TDD Best Practices)
- ✅ **Behavior-focused**: Test user outcomes, not internal implementation
- ✅ **Strategic mocking**: Mock only external dependencies
- ✅ **Test pyramid**: Unit → Integration → E2E
- ✅ **User story mapping**: Tests validate user requirements
- ✅ **Maintainable**: Tests survive refactoring

## Directory Migration Plan

The test structure is actively being improved:

1. **✅ Complete**: Mirror structure, fixtures, helpers
2. **🔄 In Progress**: Refactoring existing tests for better TDD
3. **⏳ Planned**: E2E user scenario tests, behavior-focused integration tests

## Development Workflow

For daily development, focus on:

1. **Models tests** (`python run_tests.py models`) - Always should pass
2. **Core tests** (`python run_tests.py core`) - Primary validation
3. **Timeline tests** - Track timeline logic improvements

UI tests are being refactored and may have temporary failures during the TDD improvement process.