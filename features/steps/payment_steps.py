"""
Payment Steps

Steps file for payment.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
from os import getenv
import logging
import json
import requests
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '60'))

@given('a list of payment methods')
def step_impl(context):
    """ Load a database of payment methods """
    headers = {'Content-Type': 'application/json'}
    context.resp = requests.delete(context.base_url + '/payments/reset', headers=headers)
    expect(context.resp.status_code).to_equal(204)
    create_url = context.base_url + '/payments'
    for row in context.table:
        data = {
            "order_id": int(row['order_id']),
            "customer_id": int(row['customer_id']),
            "type": row['type'],
            "available": row['available'] in ['True', 'true', '1'],
            "info": json.loads(row['info'])["info"]
            }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)

@when('I visit the "home page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)
    #context.driver.save_screenshot('home_page.png')

@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()

@when('I set the "{element_name}" to "{text_string}" in "{form}" form')
def step_impl(context, element_name, text_string, form):
    element_id = form + "_" + element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)

@then('I should see the message "{message}"')
def step_impl(context, message):
    # element = context.driver.find_element_by_id('flash_message')
    # expect(element.text).to_contain(message)
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    expect(found).to_be(True)
