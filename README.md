# Personal Assistant App

A cross-platform personal productivity application built with Kivy, designed to help users manage executive functions, emotions, and habits.

## Current Status - Phase 1: Core MVP ✅

### Completed Features

#### ✅ Navigation System
- Full screen-based navigation using Kivy ScreenManager
- Main menu with three primary modules
- Hierarchical navigation with back button support
- Smooth transitions between screens

#### ✅ Executive Function Module
**ToDo Timeline Sub-Module:**
- **To-Do List Screen**: Text input for creating task lists with "Groom my list" functionality
- **Times and Dependencies Screen**: Interface for setting time estimates and task dependencies
- **Timeline View Screen**: Visual timeline displaying current tasks, parallel tasks, and ordered task list

#### ✅ Application Architecture
- **Configurable App Title**: Easy-to-modify app branding through AppConfig class
- **Modular Structure**: Organized codebase with separate UI, core logic, and utility modules
- **Data Models**: Task and TaskManager classes for handling task organization and scheduling
- **Screen Management**: Centralized screen management with proper state handling

#### ✅ UI/UX Implementation
- Color scheme matching provided mockups
- Layout structure following design specifications
- Responsive button styling and consistent spacing
- Cross-platform compatibility through Kivy framework

### Project Structure
```
src/
├── core/
│   ├── app.py          # Main application and screen manager
│   ├── config.py       # App configuration settings
│   └── models.py       # Data models (Task, TaskManager)
├── ui/
│   ├── screens.py      # All screen implementations
│   └── main.kv         # Kivy layout file (legacy)
└── utils/
    └── __init__.py
main.py                 # Application entry point
tests/                  # Comprehensive test suite with TDD structure
```

### Technology Stack
- **GUI Framework**: Kivy 2.3.1
- **Language**: Python 3.10+
- **Testing**: pytest (configured)
- **Code Quality**: black, flake8, mypy, pre-commit

### Installation & Setup

#### Prerequisites
- Python 3.10+
- Git

#### Quick Start
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

4. **Run the application**:
   ```bash
   python main.py
   ```

### Development Workflow
- Follow strict Git workflow with feature branches
- Each GitHub issue gets its own branch and PR
- Unit tests required for all new features
- Code quality checks with black, flake8, and mypy
- Main branch always contains stable, working code

## Placeholder Modules (Coming Soon)
- **Emotions Management**: Tools for emotional regulation and tracking
- **Habits**: Habit formation and tracking system
- **Pomodoro**: Time management and focus sessions
- **Routines**: Daily routine planning and execution

## Development Status
- ✅ Phase 1: Core MVP (Navigation + Basic ToDo Timeline)
- 🔄 Phase 2: Bug fixes and feature refinements
- ⏳ Phase 3: Advanced ToDo management with AI grooming
- ⏳ Phase 4: Emotions Management module
- ⏳ Phase 5: Habits module integration

## Testing

This project uses a comprehensive test suite organized with TDD best practices.

### Quick Start
```bash
# Run core functionality tests (recommended)
python run_tests.py core

# Run all tests with logging
python run_tests.py all --save-log
```

### Test Structure
Tests mirror the src/ directory structure:
```
tests/
├── test_core/           # Tests for src/core/ (models, timeline)
├── test_ui/             # Tests for src/ui/ (screens, navigation)
├── fixtures/            # Test data and app instances
├── helpers/             # User interaction simulation
└── e2e/                 # End-to-end user scenarios (planned)
```

### Test Categories
- **`python run_tests.py core`** - Core business logic (✅ 39/40 pass)
- **`python run_tests.py models`** - Task/TaskManager classes (✅ 30/30 pass)  
- **`python run_tests.py ui`** - User interface tests (⚠️ being refactored)
- **`python run_tests.py quick`** - Fast development tests

### Test Output Logging
All test runs support `--save-log` to capture complete output:
```bash
python run_tests.py models --save-log
# Saves to: logs/test_log_YYYYMMDD_HHMMSS_models.txt
```

### Direct pytest Usage
```bash
# Run all tests
pytest

# Run specific test directory
pytest tests/test_core/

# Run with coverage
pytest --cov=src.core

# Run with HTML coverage report
pytest --cov=src --cov-report=html
```

### Code Quality
```bash
# Code formatting
black .

# Linting
flake8 .

# Type checking
mypy .
```

**Test Coverage**: 100% for core models, 90% for timeline generation

See `tests/README.md` for detailed testing documentation.

## Contributing
1. Create GitHub issue for feature/bug
2. Create feature branch from main
3. Implement changes with tests
4. Submit PR for review
5. Merge after approval and testing

## License
[License to be determined]