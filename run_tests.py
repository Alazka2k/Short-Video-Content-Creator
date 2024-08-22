import os
import sys

if __name__ == '__main__':
    # Add the current directory to the Python path
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

    # Import and run the tests from the tests folder
    from tests.run_tests import run_tests

    success = run_tests()
    sys.exit(0 if success else 1)