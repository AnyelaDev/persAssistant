#!/usr/bin/env python3
"""
Test runner script for the Personal Assistant project.
Runs tests with coverage reporting and provides different test scenarios.
"""
import sys
import subprocess
import argparse
import datetime
import os

def save_test_output(output, returncode, test_type):
    """Save test output to a log file with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"test_log_{timestamp}_{test_type}.txt"
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_path = os.path.join(log_dir, log_filename)
    
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"Test Run Log\n")
        f.write(f"{'=' * 50}\n")
        f.write(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Test Type: {test_type}\n")
        f.write(f"Exit Code: {returncode}\n")
        f.write(f"{'=' * 50}\n\n")
        f.write(output)
    
    print(f"Test output saved to: {log_path}")
    return log_path

def run_tests(test_type="all", verbose=True, save_log=False):
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
            "path": "tests/test_core/test_models.py tests/test_core/test_timeline.py",
            "description": "Run core functionality tests (models and timeline)",
            "extra_args": ["--cov=src.core"]
        },
        "models": {
            "path": "tests/test_core/test_models.py",
            "description": "Run only model tests",
            "extra_args": ["--cov=src.core.models"]
        },
        "ui": {
            "path": "tests/test_ui/test_ui_components.py tests/test_ui/test_navigation.py",
            "description": "Run UI and navigation tests"
        },
        "timeline": {
            "path": "tests/test_core/test_timeline.py",
            "description": "Run timeline generation tests"
        },
        "quick": {
            "path": "tests/test_core/test_models.py",
            "description": "Quick test run (models only)",
            "extra_args": ["--tb=line", "-q"]
        },
        "test_core": {
            "path": "tests/test_core/",
            "description": "Run all core module tests",
            "extra_args": ["--cov=src.core"]
        },
        "test_ui": {
            "path": "tests/test_ui/",
            "description": "Run all UI module tests"
        },
        "unit": {
            "path": "tests/test_core/",
            "description": "Run unit tests (business logic only)",
            "extra_args": ["--cov=src.core"]
        },
        "integration": {
            "path": "tests/test_ui/",
            "description": "Run integration tests (UI interactions)"
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
        if save_log:
            # Capture output when logging is enabled
            result = subprocess.run(cmd, check=False, capture_output=True, text=True)
            output = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
            save_test_output(output, result.returncode, test_type)
        else:
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
        choices=["all", "core", "models", "ui", "timeline", "quick", "test_core", "test_ui", "unit", "integration"],
        help="Type of tests to run (default: core)"
    )
    parser.add_argument(
        "-q", "--quiet", 
        action="store_true",
        help="Run tests in quiet mode"
    )
    parser.add_argument(
        "--save-log", 
        action="store_true",
        help="Save test output to a log file"
    )
    
    args = parser.parse_args()
    
    return run_tests(args.test_type, verbose=not args.quiet, save_log=args.save_log)

if __name__ == "__main__":
    sys.exit(main())