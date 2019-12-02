# pylint: disable=no-member
"""
Payments Store Service

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
from functools import wraps
from flask import jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes
from flask_restplus import Api, Resource, fields, reqparse, inputs
from werkzeug.exceptions import NotFound
from schemas.payment_schema import payment_schema
from schemas.payment_schema_with_id import payment_schema_with_id
from schemas.payment_schema_doc import payment_schema_doc

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from service.models import Payment, DataValidationError

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Root URL response """
    return app.send_static_file('index.html')
    # return jsonify(name='Payment REST API Service',
    #                version='1.0',
    #                paths=url_for('list_payments', _external=True)
    #                ), status.HTTP_200_OK


# Document the type of autorization required
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Api-Key'
    }
}

######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Payment Demo REST API Service',
          description='This is a sample server Payment store server.',
          default='payments',
          default_label='Payment operations',
          doc='/apidocs/',
          authorizations=authorizations
          # prefix='/api'
          )

# Define the model so that the docs reflect what can be sent
payment_model = api.schema_model('Payment', payment_schema_with_id)

create_model = api.schema_model('Create_Payment', payment_schema)

payment_model_doc = api.schema_model('Payment_doc', payment_schema_doc)

# query string arguments
payment_args = reqparse.RequestParser()
payment_args.add_argument('order_id', type=int, required=False,
                          help='List Payments by order id')
payment_args.add_argument('customer_id', type=int, required=False,
                          help='List Payments by customer id')
payment_args.add_argument('available', type=inputs.boolean, required=False,
                          help='List Payments by availability')
payment_args.add_argument('type', type=str, required=False,
                          help='List Payments by type')


######################################################################
# Special Error Handlers
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
               'status_code': status.HTTP_400_BAD_REQUEST,
               'error': 'Bad Request',
               'message': message
           }, status.HTTP_400_BAD_REQUEST


@api.errorhandler(jsonschema.exceptions.ValidationError)
def json_validation_error(error):
    """ Handles json validation error with ValidationError """
    # return bad_request(error.message)
    message = str(error.message)
    app.logger.warning(message)
    return {
               'status_code': status.HTTP_400_BAD_REQUEST,
               'error': 'Bad Request',
               'message': message
           }, status.HTTP_400_BAD_REQUEST


# @api.errorhandler(DatabaseConnectionError)
# def database_connection_error(error):
#     """ Handles Database Errors from connection attempts """
#     message = str(error)
#     app.logger.critical(message)
#     return {
#         'status_code': status.HTTP_503_SERVICE_UNAVAILABLE,
#         'error': 'Service Unavailable',
#         'message': message
#     }, status.HTTP_503_SERVICE_UNAVAILABLE


######################################################################
# Authorization Decorator
######################################################################
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-Api-Key' in request.headers:
            token = request.headers['X-Api-Key']

        if app.config.get('API_KEY') and app.config['API_KEY'] == token:
            return f(*args, **kwargs)
        else:
            return {'message': 'Invalid or missing token'}, 401

    return decorated


######################################################################
# Function to generate a random API key (good for testing)
######################################################################
def generate_apikey():
    """ Helper function used when testing API keys """
    return uuid.uuid4().hex


# ######################################################################
# # Error Handlers
# ######################################################################
@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = str(error)
    app.logger.error(message)
    return jsonify(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                   error='Internal Server Error',
                   message=message), status.HTTP_500_INTERNAL_SERVER_ERROR


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route('/healthcheck')
def healthcheck():
    """ Let them know our heart is still beating """
    return make_response(jsonify(status=200, message='Healthy'),
                         status.HTTP_200_OK)


######################################################################
#  PATH: /payments/{payment_id}
######################################################################
@api.route('/payments/<payment_id>')
@api.param('payment_id', 'The Payment identifier')
class PaymentResource(Resource):
    """
    PaymentResource class

    Allows the manipulation of a single Payment
    GET /payments/{id} - Returns a Payment with the id
    PUT /payments/{id} - Update a Payment with the id
    DELETE /payments/{id} -  Delete a Payment with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A PAYMENT
    # ------------------------------------------------------------------
    @api.doc('get_payment')
    @api.response(404, 'Payment not found')
    @api.response(200, 'Payment retrieved successfully', payment_model_doc)
    # @api.marshal_with(payment_model)
    def get(self, payment_id):
        """
        Retrieve a single Payment

        This endpoint will return a Payment based on its id
        """
        app.logger.info("Request to Retrieve a payment with id [%s]",
                        payment_id)
        payment = Payment.find(payment_id)
        if not payment:
            api.abort(status.HTTP_404_NOT_FOUND,
                      "Payment with id '{}' was not found.".format(payment_id))
        return payment.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING PAYMENT
    # ------------------------------------------------------------------
    @api.doc('update_payment', security='apikey')
    @api.response(404, 'Payment not found')
    @api.response(400, 'The posted Payment data was not valid')
    @api.response(200, 'Payment updated successfully', payment_model_doc)
    @api.expect(payment_model_doc)
    # @api.marshal_with(payment_model)
    # @token_required
    def put(self, payment_id):
        """
        Update a Payment

        This endpoint will update a Payment based the body that is posted
        """
        app.logger.info('Request to Update a payment with id [%s]', payment_id)
        check_content_type('application/json')
        payment = Payment.find(payment_id)
        if not payment:
            api.abort(status.HTTP_404_NOT_FOUND,
                      "Payment with id '{}' was not found.".format(payment_id))
        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        # still use jsonschema to validate data
        jsonschema.validate(data, payment_schema)
        payment.deserialize(data)
        payment.id = payment_id
        payment.save()
        return payment.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A PAYMENT
    # ------------------------------------------------------------------
    @api.doc('delete_payment', security='apikey')
    @api.response(204, 'Payment deleted')
    # @token_required
    def delete(self, payment_id):
        """
        Delete a Payment

        This endpoint will delete a Payment based the id specified in the path
        """
        app.logger.info('Request to Delete a payment with id [%s]', payment_id)
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
    # LIST ALL PAYMENTS
    # ------------------------------------------------------------------
    @api.doc('list_payments')
    @api.expect(payment_args, validate=True)
    @api.response(200, 'Success', [payment_model_doc])
    # @api.marshal_list_with(payment_model)
    def get(self):
        """ Returns all of the Payments """
        app.logger.info('Request to list Payments...')
        args = payment_args.parse_args()

        customer_id = args['customer_id']
        order_id = args['order_id']
        available = args['available']
        type = args['type']

        payments = Payment.find_by(customer_id, order_id, available, type)
        results = [payment.serialize() for payment in payments]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # CREATE A NEW PAYMENT
    # ------------------------------------------------------------------
    @api.doc('create_payments', security='apikey')
    @api.expect(payment_model_doc)
    @api.response(400, 'The posted data was not valid')
    @api.response(201, 'Payment created successfully', payment_model_doc)
    # @api.marshal_with(payment_model, code=201)
    # @token_required
    def post(self):
        """
        Creates a Payment
        This endpoint will create a Payment based the data in the body that
        is posted
        """
        app.logger.info('Request to Create a Payment')
        check_content_type('application/json')
        payment = Payment()
        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        # still use jsonschema to validate data
        jsonschema.validate(data, payment_schema)
        payment.deserialize(data)
        payment.save()
        app.logger.info('Payment with new id [%s] saved!', payment.id)
        location_url = api.url_for(PaymentResource, payment_id=payment.id,
                                   _external=True)
        return payment.serialize(), status.HTTP_201_CREATED, {
            'Location': location_url}


######################################################################
#  PATH: /payments/{payments_id}/toggle
######################################################################
@api.route('/payments/<int:payments_id>/toggle')
@api.param('payments_id', 'The Payment identifier')
class ToggleResource(Resource):
    """ Toggle action on a Payment """

    @api.doc('toggle_payment')
    @api.response(404, 'Payment not found')
    def patch(self, payments_id):
        """
        Toggle payment availability
        This toggles whether or not a payment is currently available
        """
        app.logger.info('Request to toggle payment availability with id: %s',
                        payments_id)
        payment = Payment.find(payments_id)
        if not payment:
            api.abort(status.HTTP_404_NOT_FOUND,
                      'Payment with id [{}] was not found.'.format(payments_id))
        payment.available = not payment.available
        payment.save()
        return payment.serialize(), status.HTTP_200_OK


######################################################################
# DELETE ALL PAYMENTS (Using for test only)
######################################################################
@app.route('/payments/reset', methods=['DELETE'])
def reset_payments():
    """ Removes all payments from the database """
    app.logger.info('Remove all the payments inside the database')
    Payment.disconnect()
    Payment.remove_all()
    return make_response('', status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Payment.init_db(app)


def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers['Content-Type'] == content_type:
        return
    app.logger.error('Invalid Content-Type: %s',
                     request.headers['Content-Type'])
    abort(415, 'Content-Type must be {}'.format(content_type))


def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print('Setting up logging...')
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.propagate = False
        app.logger.info('Logging handler established')
