Feature: The pet store service back-end
    As a Pet Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my pets

    Background:
        Given the following pets
            | order_id | customer_id | type | available | info |
            | 100 | 1 | credit card | True | {"info": {"credit_card_number": "123123123", "card_holder_name": "Amir Shirif", "expiration_month": 12, "expiration_year": 2020, "security_code": "123"}} |

Scenario: First try
  When I visit the "home page"
