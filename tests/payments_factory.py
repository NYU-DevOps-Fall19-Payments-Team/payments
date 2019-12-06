"""
Test Factory to make fake objects for testing.

"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Payment
from tests.dummy_data import DUMMY


class PaymentsFactory(factory.Factory):
    """Creates fake payments that you can't use to buy Ramen."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Class for testing the Payment class."""
        model = Payment

    order_id = factory.Sequence(lambda n: n)
    customer_id = factory.Sequence(lambda n: n)
    type = FuzzyChoice(choices=['credit card', 'paypal'])
    available = FuzzyChoice(choices=[True, False])
    info = factory.LazyAttribute(lambda o: {
        "credit card": DUMMY,
        "paypal": {
            "email": "john@example.com",
            "phone_number": "123456789",
            "token": "abc"
        }
    }[o.type])
