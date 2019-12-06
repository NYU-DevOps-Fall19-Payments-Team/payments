# pylint: disable=function-redefined, undefined-variable
# (The apparent redefinitions of step_impl and undefinedness of @given,
# @when, and @then are all handled by behave in BDD testing.)
"""
Payment Steps.

Steps file for payment.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
from os import getenv
import json
import requests
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '60'))


@given('a list of payment methods')
def step_impl(context):
    """Load a database of payment methods."""
    headers = {'Content-Type': 'application/json'}
    context.resp = requests.delete(
        context.base_url + '/payments/reset', headers=headers)
    expect(context.resp.status_code).to_equal(204)  # pylint: disable=no-member
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
        expect(context.resp.status_code).to_equal(201)  # pylint: disable=no-member


@when('I visit the "home page"')
def step_impl(context):
    """Make a call to the base URL."""
    context.driver.get(context.base_url)


@when('I press the "{button}" button')
def step_impl(context, button):
    """Click a specified button."""
    button_id = button.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()
    context.driver.save_screenshot('home_page.png')


@when('I set the "{element_name}" to "{text_string}" in "{form}" form')
def step_impl(context, element_name, text_string, form):
    """Set the value of a given element into a given type of form."""
    element_id = form + "_" + element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)
    context.driver.save_screenshot('home_page.png')


@when('I select "{text}" in the "{element_name}" dropdown in "{form}" form')
def step_impl(context, text, element_name, form):
    """Select the value of a given element in a given type of form."""
    element_id = form + '_' + element_name.lower()
    element = Select(context.driver.find_element_by_id(element_id))
    element.select_by_visible_text(text)
    context.driver.save_screenshot('dropdown.png')


@then('I should see the message "{message}"')
def step_impl(context, message):
    """Check whether an expected flash message appears."""
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'), message))
    expect(found).to_be(True)  # pylint: disable=no-member


@then('I should see the "{info}" in column "{column}" in the display card')
def step_impl(context, info, column):
    """Check whether the given info appears in the given column."""
    found = False
    WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.visibility_of_element_located((By.CLASS_NAME,
                                                           column)))
    elements = context.driver.find_elements_by_class_name(column)
    for element in elements:
        if element.text == info:
            found = True
    expect(found).to_be(True)  # pylint: disable=no-member


@then('I should not see the "{info}" in column "{column}" in the display card')
def step_impl(context, info, column):
    """Check whether the given info does not appear in the given column."""
    found = False
    WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.visibility_of_element_located((By.CLASS_NAME,
                                                           column)))
    elements = context.driver.find_elements_by_class_name(column)
    for element in elements:
        if element.text == info:
            print(element.text)
            found = True
    error_msg = "I should not see '%s' in '%s'" % (info, column)
    ensure(found, False, error_msg)
