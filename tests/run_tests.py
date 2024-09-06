import unittest
import os
import sys
from dotenv import load_dotenv
import logging

def run_tests():
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    # Load environment variables
    load_dotenv()
    logger.info("Environment variables loaded")

    # Add the src directory to the Python path
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src_dir = os.path.join(current_dir, 'src')
    sys.path.insert(0, src_dir)
    logger.info(f"Added {src_dir} to Python path")

    # Check for required API keys
    required_keys = ['OPENAI_API_KEY', 'BLACK_FOREST_API_KEY', 'ELEVENLABS_API_KEY', 'LUMA_API_KEY', 'SUNA_API_KEY']
    missing_keys = [key for key in required_keys if not os.environ.get(key)]
    
    if missing_keys:
        for key in missing_keys:
            logger.warning(f"{key} not found in environment variables")
        logger.warning("Please set all required API keys in the .env file or as environment variables")
        return False

    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(current_dir, 'unit_tests')  # Updated to use unit_tests directory
    logger.info(f"Discovering tests in {start_dir}")
    suite = loader.discover(start_dir, pattern='test_*.py')

    logger.info("Starting test run")
    runner = unittest.TextTestRunner(verbosity=2)

    # Custom test result class to log each test
    class LoggingTestResult(unittest.TextTestResult):
        def startTest(self, test):
            super().startTest(test)
            logger.info(f"Running test: {test.id()}")

        def addSuccess(self, test):
            super().addSuccess(test)
            logger.info(f"Test passed: {test.id()}")

        def addError(self, test, err):
            super().addError(test, err)
            logger.error(f"Test error: {test.id()} - {err[1]}")

        def addFailure(self, test, err):
            super().addFailure(test, err)
            logger.error(f"Test failed: {test.id()} - {err[1]}")

    result = runner.run(suite)
    
    logger.info("Test run completed")
    logger.info(f"Tests run: {result.testsRun}, Errors: {len(result.errors)}, Failures: {len(result.failures)}")

    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)