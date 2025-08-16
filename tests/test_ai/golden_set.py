"""
Golden set test cases for AI grooming validation.

These test cases represent realistic user inputs and expected behaviors
for the AI-powered todo list grooming functionality.
"""

GOLDEN_SET_TESTS = [
    {
        "name": "basic_deduplication",
        "input": "buy milk\nget bread\nbuy milk\nget groceries",
        "expected_deduplication": True,
        "expected_min_tasks": 3,
        "expected_max_tasks": 4,
        "description": "Should remove duplicate 'buy milk' entries"
    },
    {
        "name": "task_clarification",
        "input": "work on project\ndo stuff\nfixed that bug\ncall mom",
        "expected_clarification": True,
        "expected_min_tasks": 4,
        "description": "Should clarify vague tasks like 'do stuff'"
    },
    {
        "name": "task_breakdown",
        "input": "plan vacation\norganize birthday party\nclean house",
        "expected_breakdown": True,
        "expected_min_tasks": 3,
        "description": "Large tasks may be broken down into smaller ones"
    },
    {
        "name": "priority_detection",
        "input": "urgent - fix production bug\nbuy milk\npay bills tomorrow\noptional - organize photos",
        "expected_priority_detection": True,
        "expected_min_tasks": 4,
        "description": "Should detect and assign priorities based on keywords"
    },
    {
        "name": "empty_input",
        "input": "",
        "expected_success": False,
        "description": "Empty input should be handled gracefully"
    },
    {
        "name": "single_task",
        "input": "buy groceries",
        "expected_min_tasks": 1,
        "expected_max_tasks": 1,
        "description": "Single task should be preserved or clarified"
    },
    {
        "name": "long_list",
        "input": """
        1. Review quarterly reports
        2. Schedule team meeting
        3. Update project documentation
        4. Fix bug in login system
        5. Prepare presentation slides  
        6. Call client about requirements
        7. Order office supplies
        8. Review code changes
        9. Update database schema
        10. Test new features
        11. Deploy to staging
        12. Review security audit
        """.strip(),
        "expected_min_tasks": 10,
        "expected_categorization": True,
        "description": "Long lists should be organized and potentially categorized"
    },
    {
        "name": "dependencies_implicit",
        "input": "book flights\nbook hotel\npack bags\nplan vacation itinerary",
        "expected_dependency_detection": True,
        "expected_min_tasks": 4,
        "description": "Should detect implicit dependencies in vacation planning"
    }
]


def get_golden_set_by_name(name: str):
    """Get a specific golden set test case by name."""
    for test in GOLDEN_SET_TESTS:
        if test["name"] == name:
            return test
    return None


def get_basic_golden_set():
    """Get a subset of golden set tests for basic validation."""
    return [test for test in GOLDEN_SET_TESTS if test["name"] in [
        "basic_deduplication", 
        "single_task", 
        "empty_input"
    ]]


def validate_grooming_result(test_case: dict, result) -> dict:
    """
    Validate a grooming result against a golden set test case.
    
    Returns:
        dict with validation results and feedback
    """
    validation = {
        "passed": True,
        "issues": [],
        "score": 0,
        "max_score": 0
    }
    
    # Test success expectation
    if "expected_success" in test_case:
        validation["max_score"] += 1
        if result.success == test_case["expected_success"]:
            validation["score"] += 1
        else:
            validation["passed"] = False
            validation["issues"].append(f"Expected success={test_case['expected_success']}, got {result.success}")
    
    if not result.success:
        return validation  # Don't validate further if result failed
    
    # Test task count expectations
    task_count = len(result.groomed_tasks)
    
    if "expected_min_tasks" in test_case:
        validation["max_score"] += 1
        if task_count >= test_case["expected_min_tasks"]:
            validation["score"] += 1
        else:
            validation["passed"] = False
            validation["issues"].append(f"Expected min {test_case['expected_min_tasks']} tasks, got {task_count}")
    
    if "expected_max_tasks" in test_case:
        validation["max_score"] += 1
        if task_count <= test_case["expected_max_tasks"]:
            validation["score"] += 1
        else:
            validation["passed"] = False
            validation["issues"].append(f"Expected max {test_case['expected_max_tasks']} tasks, got {task_count}")
    
    # Test deduplication
    if test_case.get("expected_deduplication", False):
        validation["max_score"] += 1
        original_lines = [line.strip() for line in test_case["input"].split('\n') if line.strip()]
        if task_count < len(original_lines):
            validation["score"] += 1  # Some deduplication occurred
        else:
            validation["issues"].append("No deduplication detected")
    
    return validation