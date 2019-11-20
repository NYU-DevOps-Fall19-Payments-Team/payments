Feature: A store service back-end
    As a Goods or Services provider
    I need a RESTful catalog service
    So that I can keep track of my consumer's payment methods

Background:
    Given a list of payment methods
        | order_id | customer_id | type | available | info |
        | 100 | 1 | credit card | True | {"info": {"credit_card_number": "123123123", "card_holder_name": "Amir Shirif", "expiration_month": 12, "expiration_year": 2020, "security_code": "123"}} |
        | 101 | 2 | credit card | False | {"info": {"credit_card_number": "456456546", "card_holder_name": "Alex Crain", "expiration_month": 3, "expiration_year": 2028, "security_code": "987"}} |
        | 102 | 3 | credit card | True | {"info": {"credit_card_number": "7896987987", "card_holder_name": "Zheng Jiang", "expiration_month": 1, "expiration_year": 2026, "security_code": "675"}} |
        | 104 | 4 | credit card | False | {"info": {"credit_card_number": "4389493849", "card_holder_name": "Maoyi Luo", "expiration_month": 1, "expiration_year": 2026, "security_code": "675"}} |

Scenario: Delete a payment method
  When I visit the "home page"
  And I set the "payment_id" to "3" in "delete" form
  And I press the "Delete" button
  Then I should see the message "Payment has been Deleted!"

Scenario: Update a payment method for a credit card
  When I visit the "home page"
  And I set the "payment_id" to "1" in "update" form
  And I set the "customer_id" to "1" in "update" form
  And I set the "order_id" to "1" in "update" form
  And I select "Yes" in the "available" dropdown in "update" form
  And I select "Credit Card" in the "type" dropdown in "update" form
  And I set the "credit_card_number" to "7896987987" in "update" form
  And I set the "card_holder_name" to "Zheng Jiang" in "update" form
  And I set the "expiration_month" to "1" in "update" form
  And I set the "expiration_year" to "2026" in "update" form
  And I set the "security_code" to "675" in "update" form
  And I press the "Update" button
  Then I should see the message "Payment has been Updated!"

Scenario: Update a payment method for PayPal
  When I visit the "home page"
  And I set the "payment_id" to "4" in "update" form
  And I set the "customer_id" to "189" in "update" form
  And I set the "order_id" to "1000" in "update" form
  And I select "No" in the "available" dropdown in "update" form
  And I select "PayPal" in the "type" dropdown in "update" form
  And I set the "email" to "abc@nyu.edu" in "update" form
  And I set the "phone_number" to "9897674444" in "update" form
  And I set the "token" to "hereisyourtoken" in "update" form
  Then I should see the message "Payment has been Updated!"
