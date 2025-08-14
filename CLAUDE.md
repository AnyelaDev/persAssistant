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