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
    payments_type = FuzzyChoice(choices=['credit card', 'paypal'])
    available = FuzzyChoice(choices=[True, False])
