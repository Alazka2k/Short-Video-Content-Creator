const { exec } = require('child_process');
const path = require('path');

// Colors for console output
const colors = {
  reset: "\x1b[0m",
  bright: "\x1b[1m",
  red: "\x1b[31m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  blue: "\x1b[34m",
};

function runCommand(command, options = {}) {
  return new Promise((resolve, reject) => {
    exec(command, options, (error, stdout, stderr) => {
      if (error) {
        reject(error);
      } else {
        resolve({ stdout, stderr });
      }
    });
  });
}

async function runTests() {
  console.log(`${colors.bright}${colors.blue}Running tests...${colors.reset}\n`);

  try {
    // Run backend tests
    console.log(`${colors.yellow}Running backend tests...${colors.reset}`);
    const backendResult = await runCommand('python -m pytest tests');
    console.log(backendResult.stdout);

    // Run frontend tests
    console.log(`\n${colors.yellow}Running frontend tests...${colors.reset}`);
    const frontendResult = await runCommand('npm test', { cwd: path.join(__dirname, 'frontend') });
    console.log(frontendResult.stdout);

    console.log(`${colors.bright}${colors.green}All tests completed successfully!${colors.reset}`);
  } catch (error) {
    console.error(`${colors.bright}${colors.red}Error running tests:${colors.reset}`);
    console.error(error);
    process.exit(1);
  }
}

// Check if a specific test suite is specified
const args = process.argv.slice(2);
if (args.length > 0) {
  const testSuite = args[0].toLowerCase();
  if (testSuite === 'backend') {
    runCommand('python -m pytest tests')
      .then(result => console.log(result.stdout))
      .catch(error => {
        console.error(`${colors.bright}${colors.red}Error running backend tests:${colors.reset}`);
        console.error(error);
        process.exit(1);
      });
  } else if (testSuite === 'frontend') {
    runCommand('npm test', { cwd: path.join(__dirname, 'frontend') })
      .then(result => console.log(result.stdout))
      .catch(error => {
        console.error(`${colors.bright}${colors.red}Error running frontend tests:${colors.reset}`);
        console.error(error);
        process.exit(1);
      });
  } else {
    console.error(`${colors.bright}${colors.red}Invalid test suite specified. Use 'backend' or 'frontend'.${colors.reset}`);
    process.exit(1);
  }
} else {
  runTests();
}