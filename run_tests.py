#!/usr/bin/env python3
"""
Test runner script for the Personal Assistant project.
Runs tests with coverage reporting and provides different test scenarios.
"""
import sys
import subprocess
import argparse

def run_tests(test_type="all", verbose=True):
    """Run tests based on the specified type."""
    base_cmd = ["python", "-m", "pytest"]
    
    if verbose:
        base_cmd.append("-v")
    
    test_configs = {
        "all": {
            "path": "tests/",
            "description": "Run all tests"
        },
        "core": {
            "path": "tests/test_models.py tests/test_timeline.py",
            "description": "Run core functionality tests (models and timeline)",
            "extra_args": ["--cov=src/core"]
        },
        "models": {
            "path": "tests/test_models.py",
            "description": "Run only model tests",
            "extra_args": ["--cov=src/core/models.py"]
        },
        "ui": {
            "path": "tests/test_ui_components.py tests/test_navigation.py",
            "description": "Run UI and navigation tests"
        },
        "timeline": {
            "path": "tests/test_timeline.py",
            "description": "Run timeline generation tests"
        },
        "quick": {
            "path": "tests/test_models.py",
            "description": "Quick test run (models only)",
            "extra_args": ["--tb=line", "-q"]
        }
    }
    
    if test_type not in test_configs:
        print(f"Unknown test type: {test_type}")
        print(f"Available types: {', '.join(test_configs.keys())}")
        return 1
    
    config = test_configs[test_type]
    cmd = base_cmd + config["path"].split()
    
    if "extra_args" in config:
        cmd.extend(config["extra_args"])
    
    print(f"Running: {config['description']}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except KeyboardInterrupt:
        print("\nTest run interrupted by user")
        return 130

def main():
    parser = argparse.ArgumentParser(description="Run Personal Assistant tests")
    parser.add_argument(
        "test_type", 
        nargs="?", 
        default="core",
        choices=["all", "core", "models", "ui", "timeline", "quick"],
        help="Type of tests to run (default: core)"
    )
    parser.add_argument(
        "-q", "--quiet", 
        action="store_true",
        help="Run tests in quiet mode"
    )
    
    args = parser.parse_args()
    
    return run_tests(args.test_type, verbose=not args.quiet)

if __name__ == "__main__":
    sys.exit(main())