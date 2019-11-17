Feature: A store service back-end
    As a Goods or Services provider
    I need a RESTful catalog service
    So that I can keep track of my consumer's payment methods

    Background:
        Given a list of payment methods
            | order_id | customer_id | type | available | info |
            | 100 | 1 | credit card | True | {"info": {"credit_card_number": "123123123", "card_holder_name": "Amir Shirif", "expiration_month": 12, "expiration_year": 2020, "security_code": "123"}} |
            | 101 | 2 | credit card | False | {"info": {"credit_card_number": "456456546", "card_holder_name": "Aliya Shirif", "expiration_month": 3, "expiration_year": 2028, "security_code": "987"}} |
            | 102 | 1 | credit card | False | {"info": {"credit_card_number": "7896987987", "card_holder_name": "Amani Shirif", "expiration_month": 1, "expiration_year": 2026, "security_code": "675"}} |

Scenario: First try
  When I visit the "home page"
