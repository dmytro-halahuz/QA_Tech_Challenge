# Run once to install dependencies:
# sudo apt install npm -y
# sudo npm install -g allure
# sudo apt install python3-venv -y
# python3 -m venv .venv
# ./.venv/bin/pip install -r requirements.txt
# ./.venv/bin/playwright install
# ./.venv/bin/playwright install-deps

# Load secrets for a different env(prod is default)
#set -a
#source ./env/secrets/prod.env

# Execute tests
./.venv/bin/pytest

# Execute with a different .env file (prod is default)
#./.venv/bin/pytest --envfile ./env/prod.env

#Generate report and open in browser
allure awesome allure-results --single-file
xdg-open allure-report/index.html
