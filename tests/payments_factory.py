"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Payment

class PaymentsFactory(factory.Factory):
    """ Creates fake pets that you don't have to feed """
    class Meta:
        model = Payment
    order_id = factory.Sequence(lambda n: n)
    customer_id = factory.Sequence(lambda n: n)
    payments_type = FuzzyChoice(choices=['credit card','paypal'])
    available = FuzzyChoice(choices=[True, False])

if __name__ == '__main__':
    for _ in range(10):
        payment = PaymentsFactory()
        print(payment.serialize())