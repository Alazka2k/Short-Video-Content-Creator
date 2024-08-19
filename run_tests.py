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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, 'src')
    sys.path.insert(0, src_dir)
    logger.info(f"Added {src_dir} to Python path")

    # Check for OpenAI API key
    if not os.environ.get('OPENAI_API_KEY'):
        logger.warning("OPENAI_API_KEY not found in environment variables")
        logger.warning("Please set your OpenAI API key in the .env file or as an environment variable")
        return False

    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(current_dir, 'tests')
    logger.info(f"Discovering tests in {start_dir}")
    suite = loader.discover(start_dir, pattern='test_*.py')

    logger.info("Starting test run")
    runner = unittest.TextTestRunner(verbosity=2)

    # Custom test result class to log each test
    class LoggingTestResult(unittest.TextTestResult):
        def startTest(self, test):
            super().startTest(test)
            logger.info(f"Running test: {test.id()}")

    result = runner.run(suite)
    
    logger.info("Test run completed")
    logger.info(f"Tests run: {result.testsRun}, Errors: {len(result.errors)}, Failures: {len(result.failures)}")

    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)