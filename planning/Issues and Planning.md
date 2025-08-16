# Next Issues to Address - Phase 2

Based on manual testing feedback, here are the GitHub issues we need to create and address:

## Plan Overview

The feedback reveals several critical bugs and missing functionality that need to be addressed in Phase 2. The main areas are:
1. UI/UX improvements (navigation buttons, background colors)
2. ToDo list grooming functionality (currently missing LLM integration)
3. Data flow between screens (ToDo object creation and persistence)
4. Screen data integration (Times & Dependencies should show actual todo items)

## GitHub Issues to Create

### Issue #5: Fix Timeline Screen Navigation
**Title:** Replace "Next" button with "Home" button on Timeline screen

**Description:**
The Timeline screen currently has a "Next" button that doesn't lead anywhere meaningful. Replace it with a "Home" button that navigates back to the main menu while preserving all user data.

**Acceptance Criteria:**
- [ ] Remove "Next" button from Timeline screen
- [ ] Add "Home" button that navigates to main menu
- [ ] Ensure data persistence when navigating home
- [ ] Maintain existing "Back" button functionality

**Labels:** bug, ui/ux, navigation

---

### Issue #6: Fix Background Color Across All Screens
**Title:** Lighten background colors for better readability

**Description:**
The current background color scheme is too dark across all screens, making the app difficult to read and use.

**Acceptance Criteria:**
- [ ] Review and update background colors in all screens
- [ ] Ensure good contrast ratio for accessibility
- [ ] Maintain design consistency with mockups
- [ ] Test on different screen sizes and devices

**Labels:** bug, ui/ux, design

---

### Issue #7: Implement LLM-powered ToDo List Grooming
**Title:** Add AI-powered grooming functionality to ToDo list

**Description:**
The "Groom my list" button currently only adds numbers to items. Implement proper LLM integration to intelligently organize, clarify, and optimize todo lists.

**Acceptance Criteria:**
- [ ] Research and integrate appropriate LLM service (OpenAI, Claude, etc.)
- [ ] Implement grooming logic that:
  - [ ] Clarifies vague tasks
  - [ ] Breaks down large tasks into smaller ones
  - [ ] Removes duplicates
  - [ ] Prioritizes tasks logically
  - [ ] Improves task descriptions
- [ ] Add configuration for LLM API keys
- [ ] Handle API errors gracefully
- [ ] Add loading indicator during grooming

**Labels:** enhancement, ai, core-functionality

---

### Issue #8: Implement ToDo Object Creation from Groomed List
**Title:** Create ToDo objects with time and dependency attributes from groomed list

**Description:**
After grooming, the "Next" button should convert the groomed text into structured ToDo objects with proper attributes for time estimation and dependency management.

**Acceptance Criteria:**
- [ ] Parse groomed todo list text into individual tasks
- [ ] Create ToDo objects with attributes:
  - [ ] `title` (string)
  - [ ] `time` (hh:mm:ss format)
  - [ ] `parallelism` (boolean, default: false)
  - [ ] `dependencies` (list of ToDo object references)
- [ ] Store ToDo objects in TaskManager
- [ ] Pass data to Times and Dependencies screen
- [ ] Handle parsing errors gracefully

**Labels:** enhancement, core-functionality, data-model

---

### Issue #9: Update Times and Dependencies Screen with Real Data
**Title:** Display actual todo items in Times and Dependencies screen

**Description:**
The Times and Dependencies screen should display the actual todo items from the previous screen instead of placeholder text. Remove the unnecessary "Groom my list" button.

**Acceptance Criteria:**
- [ ] Display actual todo item titles from previous screen
- [ ] Remove "Groom my list" button (not applicable here)
- [ ] Pre-populate time and dependency fields if data exists
- [ ] Save time and dependency updates to ToDo objects
- [ ] Handle cases where no todos exist

**Labels:** enhancement, ui/ux, data-integration

---

### Issue #10: Add Unit Tests for ToDo Grooming Functionality
**Title:** Implement comprehensive tests for LLM grooming feature

**Description:**
Create unit tests to ensure the LLM grooming functionality works correctly and handles edge cases.

**Acceptance Criteria:**
- [ ] Test grooming with various input formats
- [ ] Test error handling for API failures
- [ ] Test grooming with empty/invalid inputs
- [ ] Mock LLM API calls for consistent testing
- [ ] Test grooming result parsing
- [ ] Achieve >90% code coverage for grooming module

**Labels:** testing, ai, quality-assurance

---

### Issue #11: Add Unit Tests for ToDo Object Creation
**Title:** Implement tests for ToDo object creation and management

**Description:**
Create comprehensive unit tests for the ToDo object creation process from groomed text and the TaskManager functionality.

**Acceptance Criteria:**
- [ ] Test ToDo object creation from various text formats
- [ ] Test TaskManager add/remove/update operations
- [ ] Test dependency relationship creation
- [ ] Test time parsing and validation
- [ ] Test parallelism flag handling
- [ ] Test data persistence between screens
- [ ] Achieve >90% code coverage for models module

**Labels:** testing, core-functionality, quality-assurance

---

### Issue #12: Improve Data Flow Between Screens
**Title:** Implement proper data passing and persistence between screens

**Description:**
Ensure that data flows correctly between ToDo List → Times & Dependencies → Timeline screens without loss of information.

**Acceptance Criteria:**
- [ ] Implement data persistence in ScreenManager
- [ ] Pass ToDo objects between screens
- [ ] Update Timeline screen to show real task data
- [ ] Ensure back navigation preserves changes
- [ ] Handle screen refresh without data loss

**Labels:** enhancement, architecture, data-flow

---

## Implementation Priority

1. **High Priority (Critical bugs):**
   - Issue #5: Timeline navigation fix
   - Issue #6: Background color fix
   - Issue #9: Real data in Times & Dependencies

2. **Medium Priority (Core functionality):**
   - Issue #8: ToDo object creation
   - Issue #12: Data flow between screens
   - Issue #7: LLM grooming (requires API setup)

3. **Low Priority (Quality assurance):**
   - Issue #10: Grooming tests
   - Issue #11: ToDo object tests

## Dependencies

- Issue #7 depends on LLM service selection and API key configuration
- Issue #9 depends on Issue #8 (ToDo object creation)
- Issue #10 depends on Issue #7 (grooming implementation)
- Issue #11 depends on Issue #8 (ToDo object creation)
- Issue #12 may need to be addressed alongside multiple other issues

## Estimated Timeline

- **Week 1**: Issues #5, #6, #9 (UI fixes and basic data integration)
- **Week 2**: Issues #8, #12 (Core functionality and data flow)
- **Week 3**: Issue #7 (LLM integration)
- **Week 4**: Issues #10, #11 (Testing and quality assurance)

---

## Additional Architect Feedback Integration

Based on feedback from the ML architect review (see `planning/Feedback from Architect.md`), the following improvements should be incorporated:

### New Issues to Add:

#### Issue #13: Add Basic Unit Test Foundation ✅ **COMPLETED**
**Title:** Implement basic unit tests for core functionality

**Description:**
The architect noted missing test coverage as a key weakness. Add foundational unit tests for TaskManager operations, navigation behavior, and UI instantiation to catch regressions early.

**Acceptance Criteria:**
- [x] Add tests for TaskManager logic (add/remove/update operations)
- [x] Add tests for Timeline generation functionality  
- [x] Add tests for navigation flows between screens
- [x] Add tests for UI component instantiation
- [x] Set up CI pipeline to run tests automatically
- [x] Achieve basic test coverage reporting

**Labels:** testing, foundation, quality-assurance
**Priority:** High
**Status:** ✅ COMPLETED - All 40 core tests and 24 UI tests passing with 100% coverage on models.py

---

#### Issue #14: Implement Input Validation and Error Handling
**Title:** Add robust error handling and input validation

**Description:**
Current implementation lacks input validation and error handling for edge cases. This will become critical as complexity increases in later phases.

**Acceptance Criteria:**
- [ ] Add input validation for task dependencies (no circular references)
- [ ] Add validation for time format inputs
- [ ] Implement user feedback for invalid actions
- [ ] Add error boundaries for UI components
- [ ] Handle edge cases in task creation and management
- [ ] Add fallback UI states for error conditions

**Labels:** enhancement, error-handling, robustness
**Priority:** Medium

---

#### Issue #15: Clarify and Document AI Integration Strategy
**Title:** Define detailed AI/LLM integration architecture

**Description:**
The architect highlighted that the AI integration plan needs clarity regarding prompt construction, inference location, and error handling.

**Acceptance Criteria:**
- [ ] Document prompt templates for todo grooming
- [ ] Define API handling strategy (local vs remote inference)
- [ ] Specify error fallback mechanisms if model unavailable
- [ ] Document model selection criteria and configuration
- [ ] Add API key management and security considerations
- [ ] Create integration testing strategy for AI features

**Labels:** documentation, ai, architecture
**Priority:** High (blocks Issue #7)

---

#### Issue #16: Enhance Project Documentation
**Title:** Improve project-level documentation and vision

**Description:**
Add missing project context including objectives, target user personas, broader vision, and contribution guidelines.

**Acceptance Criteria:**
- [ ] Update README with project vision and objectives
- [ ] Define target user personas and use cases
- [ ] Add contribution guidelines and coding conventions
- [ ] Document roadmap with dates and milestones
- [ ] Add usage scenarios and examples
- [ ] Include architecture overview and design decisions

**Labels:** documentation
**Priority:** Low

---

#### Issue #17: Add Project License
**Title:** Choose and implement open-source license

**Description:**
Currently marked as "to be determined" which can hinder open-source engagement and contributions.

**Acceptance Criteria:**
- [ ] Research appropriate license options (MIT, Apache 2.0, etc.)
- [ ] Choose license based on project goals
- [ ] Add LICENSE file to repository
- [ ] Update package.json/setup.py with license information
- [ ] Ensure all code headers comply with chosen license

**Labels:** legal, open-source
**Priority:** Low

---

### Updated Implementation Priority

**Critical Foundation (Week 0-1):**
- ✅ Issue #13: Basic unit tests (prerequisite for all development) - **COMPLETED**
- Issue #15: AI integration strategy (blocks AI features)
- Issue #5: Timeline navigation fix
- Issue #6: Background color fix

**Core Functionality (Week 2-3):**
- Issue #14: Error handling and validation
- Issue #8: ToDo object creation  
- Issue #9: Real data in Times & Dependencies
- Issue #12: Data flow between screens

**AI Integration (Week 3-4):**
- Issue #7: LLM grooming (after Issue #15)
- Issue #10: Grooming tests

**Quality & Documentation (Week 4-5):**
- Issue #11: ToDo object tests
- Issue #16: Enhanced documentation
- Issue #17: Project license

### Architect Recommendations Summary

The architect praised the **modular architecture**, **robust navigation**, and **development best practices** while identifying key improvement areas:

1. **Strengths to Maintain:**
   - Clear separation of concerns (core/ui/utils)
   - Screen manager implementation
   - Development tooling setup (pytest, black, flake8, mypy)
   - Git workflow recommendations

2. **Critical Gaps to Address:**
   - Missing test coverage (highest priority)
   - Lack of error handling and validation
   - Underspecified AI integration plan
   - Incomplete documentation and licensing

3. **Overall Assessment:**
   - **Impressive foundation** for a Phase 1 MVP
   - Strong structure and UI implementation
   - Ready for Phase 2 with proper foundation work