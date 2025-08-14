# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal assistant project that is currently in the initial planning phase. The codebase is empty and will be developed following a structured workflow approach.

## Development Workflow

This project follows a strict development workflow as outlined in the "Workflow specs" file:

1. **Testing Requirements**: Unit tests must be written for all code created. Tests should be run after adding new features.

2. **Version Control**: Work with git and GitHub for version control with the following structure:
   - Main branch must always remain stable with only stable code
   - Create GitHub issues for features and bugs
   - Each issue gets its own branch and PR
   - Make smaller, frequent commits in issue branches for better tracking

3. **Testing Strategy**: Implement automated tests after merges, including:
   - Unit tests for all code
   - Integration tests when appropriate
   - Performance benchmarks as the codebase evolves

4. **Progress Tracking**: Use labels to track code status hourly for benchmarking progress.

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
- Run tests: `pytest`
- Run tests with coverage: `pytest --cov`
- Format code: `black .`
- Lint code: `flake8 .`
- Type check: `mypy .`

### Technology Stack
- **GUI Framework**: Kivy
- **Testing**: pytest, pytest-cov
- **Code Quality**: black, flake8, mypy, pre-commit