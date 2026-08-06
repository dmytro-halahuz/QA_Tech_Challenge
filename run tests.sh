# sudo apt install npm -y
# sudo npm install -g allure
# sudo apt-get install python3-venv -y
# python3 -m venv .venv
# ./.venv/bin/pip install -r requirements.txt
# ./.venv/bin/playwright install
# ./.venv/bin/playwright install-deps
./.venv/bin/pytest --envfile ./env/prod.env
# allure awesome allure-results --single-file
