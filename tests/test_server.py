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
from flask_api import status    # HTTP Status Codes
#from mock import MagicMock, patch
from service.models import Payment, DataValidationError, db
from tests.payments_factory import PaymentsFactory
import service.service as service

DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://postgres:postgres@localhost:5432/postgres')

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

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        service.init_db()
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables
        self.app = service.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_payments(self, count):
        """ Factory method to create pets in bulk """
        payments = []
        for _ in range(count):
            test_payment = PaymentsFactory()
            resp = self.app.post('/payments',
                                 json=test_payment.serialize(),
                                 content_type='application/json')
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED, 'Could not create test pet')
            new_payment = resp.get_json()
            test_payment.id = new_payment['id']
            payments.append(test_payment)
        return payments

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['name'], 'Payment REST API Service')

    def test_get_payments_list(self):
        """ Get a list of Payments """
        self._create_payments(5)
        resp = self.app.get('/payments')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_payment(self):
        """ Get a single Payment """
        # get the id of a pet
        test_payment = self._create_payments(1)[0]
        resp = self.app.get('/payments/{}'.format(test_payment.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['order_id'], test_payment.order_id)
        self.assertEqual(data['customer_id'], test_payment.customer_id)
        self.assertEqual(data['available'], test_payment.available)
        self.assertEqual(data['payments_type'], test_payment.payments_type)

    # def test_get_payment_not_found(self):
    #     """ Get a Payment thats not found """
    #     resp = self.app.get('/payments/0')
    #     self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_payments(self):
        """ Create a new Payment """
        test_payment = PaymentsFactory()
        resp = self.app.post('/payments',
                             json=test_payment.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertTrue(location != None)
        # Check the data is correct
        new_payment = resp.get_json()
        self.assertEqual(new_payment['order_id'], test_payment.order_id, "order_id do not match")
        self.assertEqual(new_payment['customer_id'], test_payment.customer_id, "customer_id do not match")
        self.assertEqual(new_payment['available'], test_payment.available, "available do not match")
        self.assertEqual(new_payment['payments_type'], test_payment.payments_type, "payments_type do not match")
        # Check that the location header was correct
        resp = self.app.get(location,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_payment = resp.get_json()
        self.assertEqual(new_payment['order_id'], test_payment.order_id, "order_id do not match")
        self.assertEqual(new_payment['customer_id'], test_payment.customer_id, "customer_id do not match")
        self.assertEqual(new_payment['available'], test_payment.available, "available do not match")
        self.assertEqual(new_payment['payments_type'], test_payment.payments_type, "payments_type do not match")

    def test_query_by_order_id(self):
        """ Get the payments with given order_id"""
        test_order_id = 1
        payments = []
        for _ in range(1):
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

    def test_update_payments(self):
        """ update a payment"""
        test_payment = PaymentsFactory()
        resp = self.app.post('/payments',
                             json=test_payment.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the payment
        new_payment = resp.get_json()
        old_available = new_payment['available']
        new_payment['available'] = not old_available
        resp = self.app.put('/payments/{}'.format(new_payment['id']),
                            json=new_payment,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_payment = resp.get_json()
        self.assertEqual(new_payment['available'] , not old_available)



    
    # @patch('app.service.Pet.find_by_name')
    # def test_bad_request(self, bad_request_mock):
    #     """ Test a Bad Request error from Find By Name """
    #     bad_request_mock.side_effect = DataValidationError()
    #     resp = self.app.get('/pets', query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # @patch('app.service.Pet.find_by_name')
    # def test_mock_search_data(self, pet_find_mock):
    #     """ Test showing how to mock data """
    #     pet_find_mock.return_value = [MagicMock(serialize=lambda: {'name': 'fido'})]
    #     resp = self.app.get('/pets', query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()