# sudo apt install npm
# sudo npm install -g allure
python -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/playwright install
pytest --envfile ./env/prod.env
allure awesome allure-results --single-file
