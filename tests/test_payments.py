"""
Test cases for Payment Model
Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from service.models import Payments, DataValidationError, db
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
        Payments.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_payment(self):
        """ Create a payment and assert that it exists """
        payment = Payments(order_id="1", customer_id="1", available=True, payments_type = "credit card")
        self.assertTrue(payment != None)
        self.assertEqual(payment.id, None)
        self.assertEqual(payment.order_id, "1")
        self.assertEqual(payment.customer_id, "1")
        self.assertEqual(payment.available, True)
        self.assertEqual(payment.payments_type, "credit card")

    def test_add_a_payment(self):
        """ Create a payment and add it to the database """
        payments = Payments.all()
        self.assertEqual(payments, [])
        payment = Payments(order_id="1", customer_id="1", available=True, payments_type = "credit card")
        self.assertTrue(payment != None)
        self.assertEqual(payment.id, None)
        payment.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(payment.id, 1)
        payments = Payments.all()
        self.assertEqual(len(payments), 1)

    def test_query_payment_by_order_id(self):
        """ Create a payment with order_id = 1 and add it to the database, then try to retrieve it"""
        Payments(order_id="1", customer_id="1", available=True, payments_type = "credit card").save()
        Payments(order_id="2", customer_id="2", available=False, payments_type = "paypal").save()
        payment_in_db = Payments.find_by_order(1)
        self.assertIsNot(payment_in_db, None)
        self.assertEqual(payment_in_db[0].order_id, 1)
        self.assertEqual(payment_in_db[0].customer_id, 1)
        self.assertEqual(payment_in_db[0].available, True)
        self.assertEqual(payment_in_db[0].payments_type, "credit card")
        payment_in_db = Payments.find_by_order(2)
        self.assertIsNot(payment_in_db, None)
        self.assertEqual(payment_in_db[0].order_id, 2)
        self.assertEqual(payment_in_db[0].customer_id, 2)
        self.assertEqual(payment_in_db[0].available, False)
        self.assertEqual(payment_in_db[0].payments_type, "paypal")

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()