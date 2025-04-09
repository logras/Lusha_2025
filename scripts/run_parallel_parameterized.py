#!/usr/bin/env python3
"""
Script to run parameterized tests in parallel.
This demonstrates how to efficiently run parametrized tests in parallel.
Usage: python3 scripts/run_parallel_parameterized.py [num_workers]
"""
import os
import sys
import subprocess
import datetime

# Default number of workers if not specified
DEFAULT_WORKERS = 4

def run_parallel_tests(num_workers=DEFAULT_WORKERS):
    """Run pytest in parallel mode with the specified number of workers."""
    # Create directory for reports if it doesn't exist
    os.makedirs('reports/html', exist_ok=True)
    
    # Generate timestamp for report name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"reports/html/parallel_parameterized_report_{timestamp}.html"
    
    # Command to run tests in parallel
    cmd = [
        "python3", "-m", "pytest", 
        f"-n={num_workers}", 
        "--dist=each",  # Run each parametrized test in a separate worker
        "-v",
        f"--html={report_name}",
        "tests/test_parameterized_parallel.py"
    ]
    
    print(f"Running parallel parameterized tests with {num_workers} workers...")
    print(f"Command: {' '.join(cmd)}")
    
    # Run the command
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Print output
    print("\nSTDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("\nSTDERR:")
        print(result.stderr)
    
    print(f"\nTests completed with exit code: {result.returncode}")
    print(f"HTML report saved to: {report_name}")
    
    return result.returncode

if __name__ == "__main__":
    # Get number of workers from command line argument
    num_workers = DEFAULT_WORKERS
    if len(sys.argv) > 1:
        try:
            num_workers = int(sys.argv[1])
        except ValueError:
            print(f"Invalid number of workers: {sys.argv[1]}. Using default: {DEFAULT_WORKERS}")
    
    sys.exit(run_parallel_tests(num_workers)) 