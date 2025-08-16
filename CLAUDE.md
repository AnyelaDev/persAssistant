# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a cross-platform personal assistant application built with Kivy. The project has completed **Phase 1 - Core MVP** and is now in **Phase 2 - Bug fixes and feature refinements** with 8 active GitHub issues to address.

### Current Status: Phase 2 Development
- 🧪 Phase 1: Core MVP (Navigation + Basic ToDo Timeline) - **IN MANUAL TESTING**
- 🔄 Phase 2: Bug fixes and feature refinements - **IN PROGRESS**
- ⏳ Phase 3: Advanced ToDo management with AI grooming
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
- **Testing**: pytest, pytest-cov
- **Code Quality**: black, flake8, mypy, pre-commit

## Current Architecture

### Project Structure
```
src/
├── core/
│   ├── app.py          # Main application and screen manager
│   ├── config.py       # App configuration (configurable title)
│   └── models.py       # Data models (Task, TaskManager)
├── ui/
│   ├── screens.py      # All screen implementations
│   └── main.kv         # Legacy Kivy layout file
└── utils/
    └── __init__.py
tests/                  # TDD-structured test suite
│   ├── test_core/      # Core business logic tests
│   ├── test_ui/        # UI and navigation tests  
│   ├── fixtures/       # Test data and app instances
│   └── helpers/        # Test utility functions
planning/               # Project planning and feedback
```

### Implemented Features (Phase 1)
- **Navigation System**: ScreenManager-based navigation between all modules
- **Executive Function Module**: Complete ToDo Timeline workflow
  - ToDo List screen with grooming functionality (basic numbering)
  - Times and Dependencies input screen
  - Timeline visualization screen
- **Configurable App Title**: Easy branding changes via AppConfig
- **Data Models**: Task and TaskManager classes for task management
- **Placeholder Modules**: Emotions Management, Habits, Pomodoro, Routines

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
- **Grooming Functionality**: Located in `src/ui/screens.py` - `ToDoListScreen.groom_list()` method (basic numbering only)
- **Data Models**: `src/core/models.py` - Task and TaskManager classes
- **Current Data Flow**: ToDo List → Times & Dependencies → Timeline (needs dynamic data persistence)
- **Testing Structure**: `/tests/` directory with existing test framework setup

### 📊 Development Status
- Use `gh issue list` to check current GitHub issues status
- Refer to planning documents for detailed implementation strategies
- Check README.md for overall project status and setup instructions