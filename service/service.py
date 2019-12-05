# Copyright 2016, 2019 John Rofrano. All Rights Reserved.
#
# Adapted by A. Crain, A. Shirif, M. Luo, and Z. Jiang
# for Professor Rofrano's DevOps Project.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Payments Store Service.

Paths:
------
GET /payments - Returns a list all of the Payments
GET /payments/{id} - Returns the Payment with a given id number
POST /payments - creates a new Payment record in the database
PUT /payments/{id} - updates a Payment record in the database
DELETE /payments/{id} - deletes a Payment record in the database
"""

import sys
import uuid
import logging
import jsonschema
from flask import jsonify, request, make_response, abort
from flask_api import status  # HTTP Status Codes
from flask_restplus import Api, Resource, reqparse, inputs
from schemas.payment_schema import payment_schema
from schemas.payment_schema_doc import payment_schema_doc

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL.
from service.models import Payment, DataValidationError

# Import Flask application.
from . import app  # pylint: disable=cyclic-import


######################################################################
# Get index.
######################################################################
@app.route('/')
def index():
    """Root URL response."""
    return app.send_static_file('index.html')


# Document the type of authorization required.
AUTHORIZATIONS = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Api-Key'
    }
}

######################################################################
# Configure Swagger before initializing it.
######################################################################
api = Api(  # pylint: disable=invalid-name
    app,
    version='1.0.0',
    title='Payment Demo REST API Service',
    description='This is a sample server Payment store server.',
    default='payments',
    default_label='Payment operations',
    doc='/apidocs/',
    authorizations=AUTHORIZATIONS)

# Define the model so that the docs reflect what can be sent.
PAYMENT_MODEL_DOC = api.schema_model('Payment_doc', payment_schema_doc)

# Query string arguments.
payment_args = reqparse.RequestParser()  # pylint: disable=invalid-name
payment_args.add_argument(
    'order_id', type=int, required=False, help='List Payments by order id')
payment_args.add_argument(
    'customer_id',
    type=int,
    required=False,
    help='List Payments by customer id')
payment_args.add_argument(
    'available',
    type=inputs.boolean,
    required=False,
    help='List Payments by availability')
payment_args.add_argument(
    'type', type=str, required=False, help='List Payments by type')


######################################################################
# Special error handlers.
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """Handles Value Errors from bad data."""
    message = str(error)
    app.logger.error(message)  # pylint: disable=no-member
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': 'Bad Request',
        'message': message
    }, status.HTTP_400_BAD_REQUEST


@api.errorhandler(jsonschema.exceptions.ValidationError)
def json_validation_error(error):
    """Handles json validation error with ValidationError."""
    message = str(error.message)
    app.logger.warning(message)  # pylint: disable=no-member
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': 'Bad Request',
        'message': message
    }, status.HTTP_400_BAD_REQUEST


######################################################################
# Function to generate a random API key.
######################################################################
def generate_apikey():
    """Helper function used when testing API keys."""
    return uuid.uuid4().hex


########################################################################
# Error handlers.
########################################################################
@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """Handles unexpected server error with 500_SERVER_ERROR."""
    message = str(error)
    app.logger.error(message)  # pylint: disable=no-member
    return jsonify(
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error='Internal Server Error',
        message=message), status.HTTP_500_INTERNAL_SERVER_ERROR


######################################################################
# Health check.
######################################################################
@app.route('/healthcheck')
def healthcheck():
    """Let them know our heart is still beating."""
    return make_response(
        jsonify(status=200, message='Healthy'), status.HTTP_200_OK)


######################################################################
#  Payment ID route.
######################################################################
@api.route('/payments/<payment_id>')
@api.param('payment_id', 'The Payment identifier')
class PaymentResource(Resource):
    """PaymentResource class.

    Allows the manipulation of a single payment.
    GET /payments/{id} - Returns the identified payment.
    PUT /payments/{id} - Updates the identified payment.
    DELETE /payments/{id} -  Deletes the identified payment.
    """

    # ------------------------------------------------------------------
    # Retrieve a payment.
    # ------------------------------------------------------------------
    @api.doc('get_payment')
    @api.response(404, 'Payment not found')
    @api.response(200, 'Payment retrieved successfully', PAYMENT_MODEL_DOC)
    @staticmethod
    def get(payment_id):
        """Retrieve a single payment.

        This endpoint will return a payment based on its id.
        """
        app.logger.info(  # pylint: disable=no-member
            "Request to Retrieve a payment with id [%s]", payment_id)
        payment = Payment.find(payment_id)
        if not payment:
            api.abort(status.HTTP_404_NOT_FOUND,
                      "Payment with id '{}' was not found.".format(payment_id))
        return payment.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # Update an existing payment.
    # ------------------------------------------------------------------
    @api.doc('update_payment')
    @api.response(404, 'Payment not found')
    @api.response(400, 'The posted Payment data was not valid')
    @api.response(200, 'Payment updated successfully', PAYMENT_MODEL_DOC)
    @api.expect(PAYMENT_MODEL_DOC)
    @staticmethod
    def put(payment_id):
        """Update a payment.

        This endpoint will update a payment with the body that is posted.
        """
        app.logger.info('Request to Update a payment with id [%s]', payment_id)  # pylint: disable=no-member
        check_content_type('application/json')
        payment = Payment.find(payment_id)
        if not payment:
            api.abort(status.HTTP_404_NOT_FOUND,
                      "Payment with id '{}' was not found.".format(payment_id))
        app.logger.debug('Payload = %s', api.payload)  # pylint: disable=no-member
        data = api.payload
        # Still use jsonschema to validate data.
        jsonschema.validate(data, payment_schema)
        payment.deserialize(data)
        payment.id = payment_id
        payment.save()
        return payment.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # Delete a payment.
    # ------------------------------------------------------------------
    @api.doc('delete_payment')
    @api.response(204, 'Payment deleted')
    @staticmethod
    def delete(payment_id):
        """Delete a payment.

        This endpoint will delete a payment based the id specified in the path
        """
        app.logger.info('Request to Delete a payment with id [%s]', payment_id)  # pylint: disable=no-member
        payment = Payment.find(payment_id)
        if payment:
            payment.delete()
        return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /payments
######################################################################
@api.route('/payments', strict_slashes=False)
class PaymentCollection(Resource):
    """ Handles all interactions with collections of Payments """

    # ------------------------------------------------------------------
    # List all payments.
    # ------------------------------------------------------------------
    @api.doc('list_payments')
    @api.expect(payment_args, validate=True)
    @api.response(200, 'Success', [PAYMENT_MODEL_DOC])
    @staticmethod
    def get():
        """Returns all of the Payments."""
        app.logger.info('Request to list Payments...')  # pylint: disable=no-member
        args = payment_args.parse_args()

        customer_id = args['customer_id']
        order_id = args['order_id']
        available = args['available']
        payment_type = args['type']

        payments = Payment.find_by(customer_id, order_id, available,
                                   payment_type)
        results = [payment.serialize() for payment in payments]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # Create a new payment.
    # ------------------------------------------------------------------
    @api.doc('create_payments')
    @api.expect(PAYMENT_MODEL_DOC)
    @api.response(400, 'The posted data was not valid')
    @api.response(201, 'Payment created successfully', PAYMENT_MODEL_DOC)
    @staticmethod
    def post():
        """Creates a payment.

        This endpoint will create a payment based on the data
        posted in the body.
        """
        app.logger.info('Request to Create a Payment')  # pylint: disable=no-member
        check_content_type('application/json')
        payment = Payment()
        app.logger.debug('Payload = %s', api.payload)  # pylint: disable=no-member
        data = api.payload
        # Still use jsonschema to validate data.
        jsonschema.validate(data, payment_schema)
        payment.deserialize(data)
        payment.save()
        app.logger.info('Payment with new id [%s] saved!', payment.id)  # pylint: disable=no-member
        location_url = api.url_for(
            PaymentResource, payment_id=payment.id, _external=True)
        return payment.serialize(), status.HTTP_201_CREATED, {
            'Location': location_url
        }


######################################################################
#  PATH: /payments/{payments_id}/toggle
######################################################################
@api.route('/payments/<int:payments_id>/toggle')
@api.param('payments_id', 'The Payment identifier')
class ToggleResource(Resource):
    """Toggle action on a payment."""

    @api.doc('toggle_payment')
    @api.response(404, 'Payment not found')
    @staticmethod
    def patch(payments_id):
        """Toggle payment availability.

        This toggles whether or not a payment is currently available.
        """
        app.logger.info(  # pylint: disable=no-member
            'Request to toggle payment availability with id: %s', payments_id)
        payment = Payment.find(payments_id)
        if not payment:
            api.abort(status.HTTP_404_NOT_FOUND,
                      'Payment with id [{}] was not found.'.format(payments_id))
        payment.available = not payment.available
        payment.save()
        return payment.serialize(), status.HTTP_200_OK


######################################################################
# Delete all payments.
######################################################################
@app.route('/payments/reset', methods=['DELETE'])
def reset_payments():
    """Removes all payments from the database."""
    app.logger.info('Remove all the payments inside the database')  # pylint: disable=no-member
    Payment.disconnect()
    Payment.remove_all()
    return make_response('', status.HTTP_204_NO_CONTENT)


######################################################################
# Utility functions.
######################################################################


def init_db():
    """Initializes the SQLAlchemy app."""
    global app  # pylint: disable=global-statement, invalid-name
    Payment.init_db(app)


def check_content_type(content_type):
    """Checks that the media type is correct."""
    if request.headers['Content-Type'] == content_type:
        return
    app.logger.error(  # pylint: disable=no-member
        'Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(415, 'Content-Type must be {}'.format(content_type))


def initialize_logging(log_level=logging.INFO):
    """Initialize the default logging to STDOUT."""
    if not app.debug:
        print('Setting up logging...')
        # Set up default logging for submodules to use STDOUT.
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)

        # Remove the Flask default handlers and use our own

        # pylint: disable=no-member

        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.propagate = False
        app.logger.info('Logging handler established')

        # pylint: enable=no-member
