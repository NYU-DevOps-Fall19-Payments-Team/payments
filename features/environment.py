"""
Environment for BDD testing with behave.

"""
import os
import requests
from selenium import webdriver

WAIT_SECONDS = 120
BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')


def before_all(context):
    """Executed once before all tests."""

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")  # Open Browser in maximized mode.
    options.add_argument("disable-infobars")  # Disabling infobars.
    options.add_argument("--disable-extensions")  # Disabling extensions.
    options.add_argument("--disable-gpu")  # Applicable to windows os only.
    options.add_argument(
        "--disable-dev-shm-usage")  # Overcome limited resource problems.
    options.add_argument("--no-sandbox")  # Bypass OS security model.
    options.add_argument("--headless")
    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(WAIT_SECONDS)  # Seconds.

    context.base_url = BASE_URL


def after_all(context):
    """Executed after all tests."""
    headers = {'Content-Type': 'application/json'}
    context.resp = requests.delete(
        context.base_url + '/payments/reset', headers=headers)
    context.driver.quit()
