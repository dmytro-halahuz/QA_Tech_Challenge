# Run once to install dependencies:
 sudo apt install npm -y
 sudo npm install -g allure
 sudo apt install python3-venv -y
 python3 -m venv .venv
 ./.venv/bin/pip install -r requirements.txt
 ./.venv/bin/playwright install
 ./.venv/bin/playwright install-deps

# Load secrets for a different env(prod is default)
#set -a
#source ./env/secrets/prod.env

# Execute tests
./.venv/bin/pytest
# Headless chromium is the default browser
# Following options are available --headed --browser firefox -browser webkit --browser chromium
# Will run on multiple browsers if specified

# Execute with a different .env file (prod.env is default) --envfile ./env/prod.env

# Generate report to ./allure-report
allure awesome allure-results --single-file

# Open report in the browser
xdg-open allure-report/index.html
