# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a cross-platform personal assistant application built with Kivy. The project has completed **Phase 1 - Core MVP** and is now in **Phase 2 - Bug fixes and feature refinements** with 8 active GitHub issues to address.

### Current Status: Phase 2 Development
- ✅ Phase 1: Core MVP (Navigation + Basic ToDo Timeline) - **COMPLETED**
- ✅ Phase 2: Bug fixes, color themes, and AI-powered grooming - **COMPLETED**
- 🔄 Phase 3: Advanced ToDo management with task dependencies - **NEXT**
- ⏳ Phase 4: Emotions Management module
- ⏳ Phase 5: Habits module integration

## Development Workflow

This project follows a strict development workflow as outlined in the "Workflow specs" file:

1. **Testing Requirements**: Unit tests must be written for all code created. Tests should be run after adding new features.

2. **TDD Testing Evaluation**: Before implementing any GitHub issue, evaluate test impact:
   - **Assess Behavioral Changes**: Determine if the change affects user behaviors or workflows
   - **Analyze Current Test Coverage**: Check if existing behavioral tests cover the affected functionality
   - **Follow TDD Principles**: Test behaviors and outcomes, not implementation details
   - **Decision Criteria**:
     - ✅ **No test changes needed** if: Change only adds functionality, doesn't break existing behavior, current tests validate user outcomes
     - ⚠️  **Test updates required** if: Change modifies existing user behaviors, breaks existing workflows, adds new critical user scenarios
   - **Documentation**: Always document the testing evaluation decision and reasoning

3. **Version Control**: Work with git and GitHub for version control with the following structure:
   - Main branch must always remain stable with only stable code
   - Create GitHub issues for features and bugs
   - Each issue gets its own branch and PR
   - Make smaller, frequent commits in issue branches for better tracking
   - **When closing GitHub issues**: Update `planning/Issues and Planning.md` to mark the issue as completed:
     - Add "✅ **COMPLETED**" to the issue title
     - Change all acceptance criteria checkboxes from `[ ]` to `[x]`
     - Add completion status line with relevant details
     - Update the priority/timeline sections to reflect completion
4. **Testing Strategy**: Implement automated tests after merges, including:
   - Unit tests for all code
   - Integration tests when appropriate
   - Performance benchmarks as the codebase evolves

5. **Progress Tracking**: Use labels to track code status hourly for benchmarking progress.

## Important Guidelines

- Never fabricate or hardcode test results
- Ensure all commits are meaningful and well-documented
- Maintain clean, testable code architecture from the start
- Follow issue-branch-PR workflow for all changes

## Development Environment Setup

### Prerequisites
- Python 3.10+
- Git

### Setup Instructions for New Team Members

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd persAssistant
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Install pre-commit hooks** (optional but recommended):
   ```bash
   pre-commit install
   ```

### Testing
The project uses a comprehensive TDD-structured test suite:

- **Recommended**: `python run_tests.py core` - Core functionality tests
- **Quick tests**: `python run_tests.py quick` - Fast development validation
- **With logging**: `python run_tests.py models --save-log` - Save output to logs/
- **Direct pytest**: `pytest tests/test_core/` - Run specific test directories
- **Coverage**: `pytest --cov=src.core` - Generate coverage reports

**Test Structure**: Tests mirror src/ directory layout in `tests/test_core/` and `tests/test_ui/`
**Current Status**: ✅ 30/30 model tests pass, ✅ 9/10 timeline tests pass

### Code Quality
- Format code: `black .`
- Lint code: `flake8 .`
- Type check: `mypy .`

### Technology Stack
- **GUI Framework**: Kivy 2.3.1
- **Language**: Python 3.10+
- **AI Integration**: HuggingFace Inference API (Mistral-7B-Instruct)
- **Environment Management**: python-dotenv
- **HTTP Client**: requests (with retry logic and timeout handling)
- **Testing**: pytest, pytest-cov, responses (HTTP mocking)
- **Code Quality**: black, flake8, mypy, pre-commit

## Current Architecture

### Project Structure
```
src/
├── ai/
│   ├── config.py       # AI service configuration and API key management
│   ├── grooming_service.py  # AI-powered todo list grooming with fallback
│   └── prompts.py      # Structured prompts and template management
├── core/
│   ├── app.py          # Main application and screen manager with color properties
│   ├── config.py       # App configuration and environment variable loading
│   └── models.py       # Data models (Task, TaskManager)
├── ui/
│   ├── color_palette.py # Centralized color theme management
│   ├── screens.py      # All screen implementations with AI integration
│   └── main.kv         # Legacy Kivy layout file with app property colors
└── utils/
    └── __init__.py
tests/                  # TDD-structured test suite
│   ├── test_ai/        # AI functionality tests with golden set validation
│   ├── test_core/      # Core business logic tests
│   ├── test_ui/        # UI and navigation tests  
│   ├── fixtures/       # Test data and app instances
│   └── helpers/        # Test utility functions
planning/               # Project planning and feedback
```

### Implemented Features (Phase 1 & 2)

#### Phase 1 - Core MVP
- **Navigation System**: ScreenManager-based navigation between all modules
- **Executive Function Module**: Complete ToDo Timeline workflow
  - ToDo List screen with basic grooming functionality
  - Times and Dependencies input screen
  - Timeline visualization screen
- **Configurable App Title**: Easy branding changes via AppConfig
- **Data Models**: Task and TaskManager classes for task management
- **Placeholder Modules**: Emotions Management, Habits, Pomodoro, Routines

#### Phase 2 - Enhanced Features
- **AI-Powered Todo Grooming**: Intelligent task optimization using HuggingFace API
  - Task clarification and enhancement
  - Duplicate detection and removal
  - Priority inference from context
  - Robust error handling with fallback
- **Centralized Color Management**: ColorPalette class with app property integration
- **Improved UI/UX**: Lighter backgrounds, better contrast, consistent theming
- **Comprehensive Testing**: AI integration tests with golden set validation

## Planning and Issue Tracking

For detailed information about current development tasks and planning:

### 📋 Active Issues and Development Plan
- **Check**: `planning/Issues and Planning.md` - Contains detailed GitHub issues breakdown with priorities, dependencies, and implementation timeline
- **Active Issues**: GitHub issues #5-12 (Phase 2 bug fixes and feature refinements)

### 📝 Project Planning Documents
- **Check**: `planning/` folder for all planning documentation
- **Manual Testing Feedback**: Available in planning documents
- **Architecture Notes**: Current implementation details and next steps

### 🔍 Quick Reference for Development

#### Core Components
- **AI Grooming Service**: `src/ai/grooming_service.py` - Main AI integration with HuggingFace
- **AI Configuration**: `src/ai/config.py` - API key management and service selection
- **Prompts**: `src/ai/prompts.py` - Structured prompt templates for AI models
- **UI Integration**: `src/ui/screens.py` - `ToDoListScreen.groom_list()` method with loading states
- **Data Models**: `src/core/models.py` - Task and TaskManager classes
- **Color Management**: `src/ui/color_palette.py` - Centralized theme colors

#### AI Development Setup
- **Environment**: Copy `.env.template` to `.env` and add HuggingFace API key
- **Testing**: `pytest tests/test_ai/ -v` for AI functionality validation
- **Fallback**: Works without API key using basic grooming functionality
- **Error Handling**: Graceful degradation with retry logic and timeouts

#### Data Flow
- ToDo List (AI groomed) → Times & Dependencies → Timeline (needs dynamic data persistence)
- AI Service: Input text → HuggingFace API → JSON response → Formatted tasks
- Fallback: Input text → Basic processing → Formatted tasks

### 📊 Development Status
- Use `gh issue list` to check current GitHub issues status
- Refer to planning documents for detailed implementation strategies
- Check README.md for overall project status and setup instructions