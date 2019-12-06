"""
Test cases for Payment Model.

Test cases can be run with:
  nosetests
  coverage report -m

"""

import unittest
import os
from service.models import Payment, DataValidationError, db
from service import app
from tests.dummy_data import DUMMY

DATABASE_URI = os.getenv(
    'DATABASE_URI', 'postgres://postgres:postgres@localhost:5432/postgres')


######################################################################
#  T E S T   C A S E S
######################################################################
class TestPayments(unittest.TestCase):
    """ Test Cases for Payments """
    _test_credit_card_info = DUMMY
    _test_paypal_info = {
        "email": "test1@test1.com",
        "phone_number": "123456789",
        "token": "abcdefg"
    }

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
        Payment.init_db(app)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_payment(self):
        """ Create a payment and assert that it exists """
        payment = Payment(
            order_id="1",
            customer_id="1",
            available=True,
            type="credit card",
            info=self._test_credit_card_info)
        self.assertTrue(payment is not None)
        self.assertEqual(payment.id, None)
        self.assertEqual(payment.order_id, "1")
        self.assertEqual(payment.customer_id, "1")
        self.assertEqual(payment.available, True)
        self.assertEqual(payment.type, "credit card")
        self.assertEqual(payment.info, self._test_credit_card_info)

    def test_add_a_payment(self):
        """ Create a payment and add it to the database """
        payments = Payment.all()
        self.assertEqual(payments, [])
        payment = Payment(
            order_id="1",
            customer_id="1",
            available=True,
            type="credit card",
            info=self._test_credit_card_info)
        self.assertTrue(payment is not None)
        self.assertEqual(payment.id, None)
        payment.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(payment.id, 1)
        payments = Payment.all()
        self.assertEqual(len(payments), 1)

    def test_delete_a_payment(self):
        """ Delete a Payment """
        payment = Payment(
            order_id="1",
            customer_id="1",
            available=True,
            type="credit card",
            info=self._test_credit_card_info)
        payment.save()
        self.assertEqual(len(Payment.all()), 1)
        # delete the pet and make sure it isn't in the database
        payment.delete()
        self.assertEqual(len(Payment.all()), 0)

    def test_serialize(self):
        """ Convert a payment to JSON """
        payment = Payment(
            order_id="1",
            customer_id="1",
            available=True,
            type="credit card",
            info=self._test_credit_card_info)
        payment_json = payment.serialize()
        self.assertEqual(payment_json['order_id'], "1")
        self.assertEqual(payment_json['customer_id'], "1")
        self.assertEqual(payment_json['available'], True)
        self.assertEqual(payment_json['type'], "credit card")
        self.assertEqual(payment_json['info'], self._test_credit_card_info)

    def test_deserialize(self):
        """ Convert JSON to a payment object """
        data = {
            "order_id": "1",
            "customer_id": "1",
            "available": True,
            "type": "credit card",
            "info": DUMMY
        }
        payment = Payment()
        payment.deserialize(data)
        self.assertEqual(data['order_id'], payment.order_id)
        self.assertEqual(data['customer_id'], payment.customer_id)
        self.assertEqual(data['available'], payment.available)
        self.assertEqual(data['type'], payment.type)
        self.assertEqual(data['info'], payment.info)

    def test_deserialize_with_key_error(self):
        """ Test deserialization with KeyError """
        data = {"order_id": "1"}
        payment = Payment()
        self.assertRaises(DataValidationError, payment.deserialize, data)

    def test_deserialize_with_type_error(self):
        """ Test deserialization with TypeError """
        data = "this is not a dictionary"
        payment = Payment()
        self.assertRaises(DataValidationError, payment.deserialize, data)

    def test_find_a_payment(self):
        """ Find a payment by ID """
        saved_payment = Payment(
            order_id="1",
            customer_id="1",
            available=True,
            type="credit card",
            info=self._test_credit_card_info)
        saved_payment.save()
        # adding extra row in case the find method return something randomly
        Payment(
            order_id="2",
            customer_id="2",
            available=False,
            type="paypal",
            info=self._test_paypal_info).save()
        payment = Payment.find(saved_payment.id)
        self.assertIsNot(payment, None)
        self.assertEqual(payment.id, saved_payment.id)
        self.assertEqual(payment.order_id, saved_payment.order_id)
        self.assertEqual(payment.customer_id, saved_payment.customer_id)
        self.assertEqual(payment.available, saved_payment.available)
        self.assertEqual(payment.type, saved_payment.type)
        self.assertEqual(payment.info, saved_payment.info)

    def _add_two_test_payments(self):
        Payment(
            order_id="1",
            customer_id="1",
            available=True,
            type="credit card",
            info=self._test_credit_card_info).save()
        Payment(
            order_id="2",
            customer_id="2",
            available=False,
            type="paypal",
            info=self._test_paypal_info).save()

    def _assert_equal_test_payment_1(self, payment):
        self.assertEqual(payment.order_id, 1)
        self.assertEqual(payment.customer_id, 1)
        self.assertEqual(payment.available, True)
        self.assertEqual(payment.type, "credit card")
        self.assertEqual(payment.info, self._test_credit_card_info)

    def _assert_equal_test_payment_2(self, payment):
        self.assertEqual(payment.order_id, 2)
        self.assertEqual(payment.customer_id, 2)
        self.assertEqual(payment.available, False)
        self.assertEqual(payment.type, "paypal")
        self.assertEqual(payment.info, self._test_paypal_info)

    def test_find_by_order(self):
        """ Find Payments by order id """
        self._add_two_test_payments()
        payments = Payment.find_by_order(1)
        self.assertIsNot(payments, None)
        self._assert_equal_test_payment_1(payments[0])
        payments = Payment.find_by_order(2)
        self.assertIsNot(payments, None)
        self._assert_equal_test_payment_2(payments[0])

    def test_find_by_customer(self):
        """ Find Payments by customer id """
        self._add_two_test_payments()
        payments = Payment.find_by_customer(1)
        self.assertIsNot(payments, None)
        self._assert_equal_test_payment_1(payments[0])
        payments = Payment.find_by_customer(2)
        self.assertIsNot(payments, None)
        self._assert_equal_test_payment_2(payments[0])

    def test_find_by_availability(self):
        """ Find Payments by availability """
        self._add_two_test_payments()
        payments = Payment.find_by_availability(True)
        self.assertIsNot(payments, None)
        self._assert_equal_test_payment_1(payments[0])
        payments = Payment.find_by_availability(False)
        self.assertIsNot(payments, None)
        self._assert_equal_test_payment_2(payments[0])

    def test_find_by_type(self):
        """ Find Payments by type"""
        self._add_two_test_payments()
        payments = Payment.find_by_type("credit card")
        self.assertIsNot(payments, None)
        self._assert_equal_test_payment_1(payments[0])
        payments = Payment.find_by_type("paypal")
        self.assertIsNot(payments, None)
        self._assert_equal_test_payment_2(payments[0])

    def test_remove_all(self):
        """ Test dropping and recreating all tables in the database """
        self._add_two_test_payments()
        self.assertEqual(len(Payment.all()), 2)
        Payment.disconnect()
        Payment.remove_all()
        self.assertEqual(len(Payment.all()), 0)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
