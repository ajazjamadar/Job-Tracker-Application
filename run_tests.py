"""
Test runner script
Run all tests with: python run_tests.py
Run specific test: python run_tests.py tests/test_auth.py
"""
import sys
import pytest

if __name__ == '__main__':
    # Default args: verbose mode
    args = ['-v']
    
    # Add any command line arguments
    if len(sys.argv) > 1:
        args.extend(sys.argv[1:])
    
    # Run pytest
    exit_code = pytest.main(args)
    sys.exit(exit_code)
