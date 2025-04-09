#!/usr/bin/env python3
"""
Script to run parametrized Selenium tests with controlled parallel execution.
This script provides options for running tests in different modes and configurations.
"""

import os
import sys
import argparse
import subprocess
import logging
import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run Selenium tests with parametrization")
    
    parser.add_argument(
        "--test", 
        default="test_apply_cv_parametrized.py",
        help="Test file to run (default: test_apply_cv_parametrized.py)"
    )
    
    parser.add_argument(
        "--parallel", 
        type=int, 
        default=0,
        help="Number of parallel processes (0 for sequential, default: 0)"
    )
    
    parser.add_argument(
        "--dist-mode", 
        choices=["each", "loadfile", "loadscope"], 
        default="loadfile",
        help="Distribution mode for pytest-xdist (default: loadfile)"
    )
    
    parser.add_argument(
        "--browser", 
        choices=["chrome", "firefox", "edge"], 
        default="chrome",
        help="Browser to use for testing (default: chrome)"
    )
    
    parser.add_argument(
        "--report-dir", 
        default="reports/html",
        help="Directory for HTML reports (default: reports/html)"
    )
    
    parser.add_argument(
        "--skip-cleanup", 
        action="store_true",
        help="Skip cleanup of temporary browser profiles"
    )
    
    parser.add_argument(
        "--markers", 
        default="nondestructive",
        help="Pytest markers to run (default: nondestructive)"
    )
    
    return parser.parse_args()

def ensure_directory_exists(directory_path):
    """Ensure that a directory exists, creating it if necessary."""
    Path(directory_path).mkdir(parents=True, exist_ok=True)
    logger.info(f"Ensured directory exists: {directory_path}")

def run_tests(args):
    """Run the tests with the specified configuration."""
    # Create timestamp for report naming
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Ensure report directory exists
    ensure_directory_exists(args.report_dir)
    
    # Build the command
    cmd = ["python3", "-m", "pytest", f"tests/{args.test}"]
    
    # Add parallelism if specified
    if args.parallel > 0:
        cmd.extend(["-n", str(args.parallel), f"--dist={args.dist_mode}"])
    
    # Add browser configuration
    os.environ["BROWSER"] = args.browser
    
    # Add markers
    if args.markers:
        cmd.extend(["-m", args.markers])
    
    # Add HTML report
    report_path = f"{args.report_dir}/report_{timestamp}.html"
    cmd.extend(["--html", report_path, "--self-contained-html"])
    
    # Add verbose output
    cmd.append("-v")
    
    # Log the command
    logger.info(f"Running command: {' '.join(cmd)}")
    
    # Run the command
    try:
        process = subprocess.run(cmd, check=True)
        logger.info(f"Tests completed with exit code: {process.returncode}")
        logger.info(f"Report generated at: {report_path}")
        return process.returncode
    except subprocess.CalledProcessError as e:
        logger.error(f"Tests failed with exit code: {e.returncode}")
        return e.returncode
    finally:
        if not args.skip_cleanup:
            cleanup_temp_profiles()

def cleanup_temp_profiles():
    """Clean up temporary browser profiles."""
    logger.info("Cleaning up temporary browser profiles...")
    
    # Temporary directory patterns to clean
    temp_patterns = [
        "/tmp/chrome_profile_*",
        "/tmp/firefox_profile_*",
        "/tmp/edge_profile_*"
    ]
    
    for pattern in temp_patterns:
        try:
            # Use subprocess to run the rm command
            subprocess.run(["rm", "-rf", pattern], check=False)
        except Exception as e:
            logger.warning(f"Error cleaning up {pattern}: {e}")
    
    logger.info("Cleanup completed")

if __name__ == "__main__":
    args = parse_args()
    logger.info(f"Starting test run with arguments: {args}")
    
    # Print configuration summary
    print("\n" + "="*80)
    print(f"Test Configuration:")
    print(f"  Test file:      tests/{args.test}")
    print(f"  Browser:        {args.browser}")
    print(f"  Parallel:       {'No' if args.parallel == 0 else f'Yes ({args.parallel} workers)'}")
    if args.parallel > 0:
        print(f"  Dist mode:      {args.dist_mode}")
    print(f"  Markers:        {args.markers}")
    print(f"  Report dir:     {args.report_dir}")
    print(f"  Skip cleanup:   {'Yes' if args.skip_cleanup else 'No'}")
    print("="*80 + "\n")
    
    # Run the tests
    exit_code = run_tests(args)
    
    # Exit with the same code as the test run
    sys.exit(exit_code) 