## Requirements
- Ubuntu or similar

### To run the tests:
```bash
git clone https://github.com/dmytro-halahuz/QA_Tech_Challenge.git
cd QA_Tech_Challenge
./run_tests.sh
```
The [script](run_tests.sh) installs all dependencies, executes the tests and presents the test report in the browser.

Environments and browsers can be configured in [run_tests.sh](run_tests.sh)

By default, the tests run against the prod env, see [env](env) folder.

Headless chromium is used by default.
