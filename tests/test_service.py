# pylint: disable=no-member
"""
Payments API Service Test Suite
Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN
"""

import unittest
import os
import logging
from flask_api import status  # HTTP Status Codes
from mock import patch
from service.models import DataValidationError, db
from service.service import internal_server_error
import service.service as service
from tests.payments_factory import PaymentsFactory

DATABASE_URI = os.getenv(
    'DATABASE_URI', 'postgres://postgres:postgres@localhost:5432/postgres')


######################################################################
#  T E S T   C A S E S
######################################################################
class TestPaymentsServer(unittest.TestCase):
    """ Payments Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        service.app.debug = False
        service.initialize_logging(logging.INFO)
        # Set up the test database
        service.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
        service.init_db()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = service.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_payments(self, count):
        """ Factory method to create payments in bulk """
        payments = []
        for _ in range(count):
            test_payment = PaymentsFactory()
            resp = self.app.post('/payments',
                                 json=test_payment.serialize(),
                                 content_type='application/json')
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED,
                             'Could not create test pet')
            new_payment = resp.get_json()
            test_payment.id = new_payment['id']
            payments.append(test_payment)
        return payments

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_payment_list(self):
        """ Get a list of Payments """
        self._create_payments(5)
        resp = self.app.get('/payments')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def _assert_equal_payment(self, data, payment):
        self.assertEqual(data['order_id'], payment.order_id,
                         "order_id do not match")
        self.assertEqual(data['customer_id'], payment.customer_id,
                         "customer_id do not match")
        self.assertEqual(data['available'], payment.available,
                         "available do not match")
        self.assertEqual(data['type'], payment.type,
                         "type do not match")
        self.assertEqual(data['info'], payment.info,
                         "info do not match")

    def test_get_payment(self):
        """ Get a single Payment """
        # get the id of a pet
        test_payment = self._create_payments(1)[0]
        resp = self.app.get('/payments/{}'.format(test_payment.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self._assert_equal_payment(resp.get_json(), test_payment)

    def test_get_payment_not_found(self):
        """ Get a Payment that's not found """
        resp = self.app.get('/payments/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_payment(self):
        """ Create a new Payment """
        test_payment = PaymentsFactory()
        resp = self.app.post('/payments',
                             json=test_payment.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertTrue(location is not None)
        # Check the data is correct
        self._assert_equal_payment(resp.get_json(), test_payment)
        # Check that the location header was correct
        resp = self.app.get(location, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self._assert_equal_payment(resp.get_json(), test_payment)

    def test_query_by_order_id(self):
        """ Get the payments with given order_id """
        test_order_id = 1
        payments = []
        for _ in range(5):
            payment = PaymentsFactory()
            payment.order_id = test_order_id
            payments.append(payment)
            self.app.post('/payments',
                          json=payment.serialize(),
                          content_type='application/json')
        resp = self.app.get('/payments',
                            query_string='order_id={}'.format(test_order_id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(payments))
        # check the data just to be sure
        for payment in data:
            self.assertEqual(payment['order_id'], test_order_id)

    def test_query_by_customer_id(self):
        """ Get the payments with given customer_id """
        test_customer_id = 1
        payments = []
        for _ in range(5):
            payment = PaymentsFactory()
            payment.customer_id = test_customer_id
            payments.append(payment)
            self.app.post('/payments',
                          json=payment.serialize(),
                          content_type='application/json')
        resp = self.app.get(
            '/payments',
            query_string='customer_id={}'.format(test_customer_id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(payments))
        # check the data just to be sure
        for payment in data:
            self.assertEqual(payment['customer_id'], test_customer_id)

    def test_query_by_availability(self):
        """ Get the payments with given availability """
        test_available = True
        payments = []
        for _ in range(5):
            payment = PaymentsFactory()
            payment.available = test_available
            payments.append(payment)
            self.app.post('/payments',
                          json=payment.serialize(),
                          content_type='application/json')
        resp = self.app.get(
            '/payments',
            query_string='available={}'.format(test_available))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(payments))
        # check the data just to be sure
        for payment in data:
            self.assertEqual(payment['available'], test_available)

    def test_query_by_type(self):
        """ Get the payments with given type """
        test_type = 'credit card'
        payments = []
        for _ in range(5):
            payment = PaymentsFactory()
            if payment.type == test_type:
                payments.append(payment)
            self.app.post('/payments',
                          json=payment.serialize(),
                          content_type='application/json')
        resp = self.app.get(
            '/payments',
            query_string='type={}'.format(test_type))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(payments))
        # check the data just to be sure
        for payment in data:
            self.assertEqual(payment['type'], test_type)

    def test_update_payment(self):
        """ Update a payment"""
        payment = PaymentsFactory()
        resp = self.app.post('/payments',
                             json=payment.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the payment
        payment_id = resp.get_json()['id']
        updated_payment = PaymentsFactory()
        resp = self.app.put('/payments/{}'.format(payment_id),
                            json=updated_payment.serialize(),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self._assert_equal_payment(resp.get_json(), updated_payment)

    def test_update_payment_not_found(self):
        """ Update a payment that does not exist """
        test_payment = PaymentsFactory()
        test_payment.id = 1
        resp = self.app.put('/payments/1', json=test_payment.serialize(),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_payment(self):
        """ Delete a Payment """
        test_payment = self._create_payments(1)[0]
        resp = self.app.delete('/payments/{}'.format(test_payment.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get('/payments/{}'.format(test_payment.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_toggle_payment_availability(self):
        """ Toggle payment availability """
        payment = PaymentsFactory()
        resp = self.app.post('/payments',
                             json=payment.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # toggle availability
        payment_id = resp.get_json()['id']
        payment.available = not payment.available
        resp = self.app.patch('/payments/{}/toggle'.format(payment_id),
                            # json=payment.serialize(),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_payment = resp.get_json()
        self.assertEqual(new_payment['available'], payment.available)

    def test_reset_payments(self):
        """ Removes all payments from the database """
        self._create_payments(2)
        resp = self.app.get('/payments')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 2)
        resp = self.app.delete('/payments/reset',
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        resp = self.app.get('/payments')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 0)

    def test_toggle_payment_availability_not_found(self):
        """ Toggle the availability of a payment that does not exist """
        payment_id = 1
        resp = self.app.patch('/payments/{}/toggle'.format(payment_id))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_wrong_type(self):
        """
        Test post request with content_type not equal to application/json
        """
        resp = self.app.post('/payments', content_type='Text')
        self.assertEqual(resp.status_code,
                         status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_wrong_method(self):
        """ Test sending a put request to '/' """
        resp = self.app.post('/', content_type='Text')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch('service.models.Payment.deserialize')
    def test_bad_request_data_validation_error(self, bad_request_mock):
        """ Test a bad request with DataValidationError """
        bad_request_mock.side_effect = DataValidationError()
        payment = PaymentsFactory()
        resp = self.app.post('/payments',
                             json=payment.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_request_json_validation_error(self):
        """ Test a bad request with json ValidationError """
        data = {
            "order_id": 1,
            "customer_id": 1,
            "type": "paypal",  # wrong type
            "available": True,
            "info": {
                "credit_card_number": "1234567890",
                "card_holder_name": "John Doe",
                "expiration_month": 4,
                "expiration_year": 2022,
                "security_code": "1234"
            }
        }
        resp = self.app.post('/payments',
                             json=data,
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('service.models.Payment.find_by')
    def test_internal_server_error(self, bad_request_mock):
        """ Test a request with internal_server_error """
        bad_request_mock.side_effect = internal_server_error("")
        resp = self.app.get('/payments', query_string='customer_id=1')
        self.assertEqual(resp.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
