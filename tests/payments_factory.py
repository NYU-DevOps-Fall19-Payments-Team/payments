"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Payment


class PaymentsFactory(factory.Factory):
    """ Creates fake payments """

    class Meta:
        model = Payment

    order_id = factory.Sequence(lambda n: n)
    customer_id = factory.Sequence(lambda n: n)
    payments_type = FuzzyChoice(choices=['credit card', 'paypal'])
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
    }[o.payments_type])


if __name__ == '__main__':
    for _ in range(10):
        payment = PaymentsFactory()
        print(payment.serialize())
