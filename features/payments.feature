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
            | 200 | 1 | paypal | True | {"info": {"email": "cool@gmail.com", "phone_number": "(896) 734-6080", "token": 12}} |
            | 201 | 2 | paypal | False | {"info": {"email": "awesome@hotmail.com", "phone_number": "(246) 719-6381", "token": 3}} |
            | 202 | 3 | paypal | True | {"info": {"email": "great@outlook.com", "phone_number": "(292) 536-5570", "token": 1} |
            | 204 | 4 | paypal | False | {"info": {"email": "prefect@icloude.com", "phone_number": "(631) 714-8611", "token": 1} |

Scenario: Read all the payments
    When I visit the "home page"
    Then I should see the 

Scenario: Delete a payment method
  When I visit the "home page"
  And I set the "ID" to "3" in "delete" form
  And I press the "Delete" button
  Then I should see the message "Payment has been Deleted!"
