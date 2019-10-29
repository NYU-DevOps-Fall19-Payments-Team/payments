"""
Test cases for Payment Model
Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from service.models import Payment, DataValidationError, db
from tests.payments_factory import PaymentsFactory
from service import app

DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://postgres:postgres@localhost:5432/postgres')


######################################################################
#  T E S T   C A S E S
######################################################################
class TestPayments(unittest.TestCase):
    """ Test Cases for Payments """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        Payment.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_payment(self):
        """ Create a payment and assert that it exists """
        payment = Payment(order_id="1", customer_id="1", available=True,
                          payments_type="credit card",
                          info={"card_number": 12345, "exp_date": "2025-10-29"})
        self.assertTrue(payment is not None)
        self.assertEqual(payment.id, None)
        self.assertEqual(payment.order_id, "1")
        self.assertEqual(payment.customer_id, "1")
        self.assertEqual(payment.available, True)
        self.assertEqual(payment.payments_type, "credit card")
        self.assertEqual(payment.info,
                         {"card_number": 12345, "exp_date": "2025-10-29"})

    def test_serialize(self):
        """ Convert a payment to JSON"""
        payment = Payment(order_id="1", customer_id="1", available=True,
                          payments_type="credit card",
                          info={"card_number": 12345, "exp_date": "2025-10-29"})
        payment_json = payment.serialize()
        self.assertEqual(payment_json['order_id'], "1")
        self.assertEqual(payment_json['customer_id'], "1")
        self.assertEqual(payment_json['available'], True)
        self.assertEqual(payment_json['payments_type'], "credit card")
        self.assertEqual(payment_json['info'],
                         {"card_number": 12345, "exp_date": "2025-10-29"})

    def test_deserialize(self):
        """ Convert a JSON to payment object"""
        data = {
            "order_id": "1",
            "customer_id": "1",
            "available": True,
            "payments_type": "credit card",
            "info": {"account_number": 123, "token": "abc"}
        }
        payment = Payment()
        payment.deserialize(data)
        self.assertEqual(data['order_id'], payment.order_id)
        self.assertEqual(data['customer_id'], payment.customer_id)
        self.assertEqual(data['available'], payment.available)
        self.assertEqual(data['payments_type'], payment.payments_type)
        self.assertEqual(data['info'], payment.info)

    def test_bad_data_deserialize(self):
        """ Test bad data """
        data = "this is not a dictionary"
        payment = Payment()
        self.assertRaises(DataValidationError, payment.deserialize, data)

    def test_delete_a_payment(self):
        """ Delete a Payment """
        payment = Payment(order_id="1", customer_id="1", available=True,
                          payments_type="credit card",
                          info={"card_number": 12345, "exp_date": "2025-10-29"})
        payment.save()
        self.assertEqual(len(Payment.all()), 1)
        # delete the pet and make sure it isn't in the database
        payment.delete()
        self.assertEqual(len(Payment.all()), 0)

    def test_find_a_payment(self):
        """ Find a payment by ID"""
        payment = Payment(order_id="1", customer_id="1", available=True,
                          payments_type = "credit card",
                          info={"card_number": 12345, "exp_date": "2025-10-29"})
        payment.save()
        #adding extra row in case the find method return something randomly
        Payment(order_id="2", customer_id="2", available=False,
                payments_type = "paypal",
                info={"account_number": 123, "token": "abc"}).save()
        self.assertTrue(payment is not None)
        self.assertIsNot(payment.id, None)
        new_payment = Payment.find(payment.id)
        self.assertEqual(new_payment.id, payment.id)

    def test_add_a_payment(self):
        """ Create a payment and add it to the database """
        payments = Payment.all()
        self.assertEqual(payments, [])
        payment = Payment(order_id="1", customer_id="1", available=True,
                          payments_type="credit card",
                          info={"card_number": 12345, "exp_date": "2025-10-29"})
        self.assertTrue(payment is not None)
        self.assertEqual(payment.id, None)
        payment.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(payment.id, 1)
        payments = Payment.all()
        self.assertEqual(len(payments), 1)

    def test_find_by_order(self):
        """ Find Payments by order id"""
        Payment(order_id="1", customer_id="1", available=True,
                payments_type="credit card",
                info={"card_number": 12345, "exp_date": "2025-10-29"}).save()
        Payment(order_id="2", customer_id="2", available=False,
                payments_type="paypal",
                info={"account_number": 123, "token": "abc"}).save()
        payment_in_db = Payment.find_by_order(1)
        self.assertIsNot(payment_in_db, None)
        self.assertEqual(payment_in_db[0].order_id, 1)
        self.assertEqual(payment_in_db[0].customer_id, 1)
        self.assertEqual(payment_in_db[0].available, True)
        self.assertEqual(payment_in_db[0].payments_type, "credit card")
        self.assertEqual(payment_in_db[0].info,
                         {"card_number": 12345, "exp_date": "2025-10-29"})
        payment_in_db = Payment.find_by_order(2)
        self.assertIsNot(payment_in_db, None)
        self.assertEqual(payment_in_db[0].order_id, 2)
        self.assertEqual(payment_in_db[0].customer_id, 2)
        self.assertEqual(payment_in_db[0].available, False)
        self.assertEqual(payment_in_db[0].payments_type, "paypal")
        self.assertEqual(payment_in_db[0].info,
                         {"account_number": 123, "token": "abc"})

    def test_find_by_customer(self):
        """ Find Payments by customer id"""
        Payment(order_id="1", customer_id="2", available=True,
                payments_type="credit card",
                info={"card_number": 12345, "exp_date": "2025-10-29"}).save()
        Payment(order_id="3", customer_id="4", available=False,
                payments_type="paypal",
                info={"account_number": 123, "token": "abc"}).save()
        payment_in_db = Payment.find_by_customer(2)
        self.assertIsNot(payment_in_db, None)
        self.assertEqual(payment_in_db[0].order_id, 1)
        self.assertEqual(payment_in_db[0].customer_id, 2)
        self.assertEqual(payment_in_db[0].available, True)
        self.assertEqual(payment_in_db[0].payments_type, "credit card")
        self.assertEqual(payment_in_db[0].info,
                         {"card_number": 12345, "exp_date": "2025-10-29"})
        payment_in_db = Payment.find_by_customer(4)
        self.assertIsNot(payment_in_db, None)
        self.assertEqual(payment_in_db[0].order_id, 3)
        self.assertEqual(payment_in_db[0].customer_id, 4)
        self.assertEqual(payment_in_db[0].available, False)
        self.assertEqual(payment_in_db[0].payments_type, "paypal")
        self.assertEqual(payment_in_db[0].info,
                         {"account_number": 123, "token": "abc"})

    def test_find_by_type(self):
        """ Find Payments by type"""
        Payment(order_id="1", customer_id="1", available=True,
                payments_type="credit card",
                info={"card_number": 12345, "exp_date": "2025-10-29"}).save()
        Payment(order_id="2", customer_id="1", available=False,
                payments_type="paypal",
                info={"account_number": 123, "token": "abc"}).save()
        Payment(order_id="3", customer_id="2", available=False,
                payments_type="credit card",
                info={"card_number": 67890, "exp_date": "2022-01-15"}).save()
        Payment(order_id="4", customer_id="2", available=True,
                payments_type="paypal",
                info={"account_number": 456, "token": "def"}).save()
        payment_in_db = Payment.find_by_type("credit card")
        self.assertIsNot(payment_in_db, None)
        self.assertEqual(payment_in_db[0].order_id, 1)
        self.assertEqual(payment_in_db[0].customer_id, 1)
        self.assertEqual(payment_in_db[0].available, True)
        self.assertEqual(payment_in_db[0].payments_type, "credit card")
        self.assertEqual(payment_in_db[0].info,
                         {"card_number": 12345, "exp_date": "2025-10-29"})
        self.assertEqual(payment_in_db[1].order_id, 3)
        self.assertEqual(payment_in_db[1].customer_id, 2)
        self.assertEqual(payment_in_db[1].available, False)
        self.assertEqual(payment_in_db[1].payments_type, "credit card")
        self.assertEqual(payment_in_db[1].info,
                         {"card_number": 67890, "exp_date": "2022-01-15"})
        payment_in_db = Payment.find_by_type("paypal")
        self.assertIsNot(payment_in_db, None)
        self.assertEqual(payment_in_db[0].order_id, 2)
        self.assertEqual(payment_in_db[0].customer_id, 1)
        self.assertEqual(payment_in_db[0].available, False)
        self.assertEqual(payment_in_db[0].payments_type, "paypal")
        self.assertEqual(payment_in_db[0].info,
                         {"account_number": 123, "token": "abc"})
        self.assertEqual(payment_in_db[1].order_id, 4)
        self.assertEqual(payment_in_db[1].customer_id, 2)
        self.assertEqual(payment_in_db[1].available, True)
        self.assertEqual(payment_in_db[1].payments_type, "paypal")
        self.assertEqual(payment_in_db[1].info,
                         {"account_number": 456, "token": "def"})


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
