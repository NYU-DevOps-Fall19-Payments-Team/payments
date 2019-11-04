# pylint: disable=too-few-public-methods
"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Payment


class PaymentsFactory(factory.Factory):
    """ Creates fake payments that you can't use to buy Ramen """

    class Meta:
        """ Class for testing the Payment class """
        model = Payment

    order_id = factory.Sequence(lambda n: n)
    customer_id = factory.Sequence(lambda n: n)
    type = FuzzyChoice(choices=['credit card', 'paypal'])
    available = FuzzyChoice(choices=[True, False])
    info = factory.LazyAttribute(lambda o: {
        "credit card": {
            "credit_card_number": "1234567890",
            "card_holder_name": "John Doe",
            "expiration_month": 4,
            "expiration_year": 2022,
            "security_code": "1234"
        },
        "paypal": {
            "email": "john@example.com",
            "phone_number": "123456789",
            "token": "abc"
        }
    }[o.type])
