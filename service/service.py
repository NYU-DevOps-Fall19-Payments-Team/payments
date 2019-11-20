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
import logging
import jsonschema
from flask import jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound
from schemas.payment_schema import payment_schema

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from service.models import Payment, DataValidationError

# Import Flask application
from . import app


######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def data_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)


@app.errorhandler(jsonschema.exceptions.ValidationError)
def json_validation_error(error):
    """ Handles json validation error with ValidationError """
    return bad_request(error.message)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """ Handles bad requests with 400_BAD_REQUEST """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_400_BAD_REQUEST,
                   error='Bad Request',
                   message=message), status.HTTP_400_BAD_REQUEST


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_404_NOT_FOUND,
                   error='Not Found',
                   message=message), status.HTTP_404_NOT_FOUND


@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """ Handles unsupported HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_405_METHOD_NOT_ALLOWED,
                   error='Method not Allowed',
                   message=message), status.HTTP_405_METHOD_NOT_ALLOWED


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def media_type_not_supported(error):
    """ Handles unsupported media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                   error='Unsupported media type',
                   message=message), status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = str(error)
    app.logger.error(message)
    return jsonify(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                   error='Internal Server Error',
                   message=message), status.HTTP_500_INTERNAL_SERVER_ERROR


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


######################################################################
# LIST ALL PAYMENT
######################################################################
@app.route('/payments', methods=['GET'])
def list_payments():
    """ Returns all of the Payments """
    app.logger.info('Request for payments list')
    # payments = []
    customer_id = request.args.get('customer_id')
    order_id = request.args.get('order_id')
    if customer_id:
        app.logger.info('Request for payments list with customer_id : %s',
                        customer_id)
        payments = Payment.find_by_customer(customer_id)
    elif order_id:
        app.logger.info('Request for payments list with order_id : %s',
                        order_id)
        payments = Payment.find_by_order(order_id)
    else:
        payments = Payment.all()

    results = [payment.serialize() for payment in payments]
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# RETRIEVE A PAYMENTS
######################################################################
@app.route('/payments/<int:payments_id>', methods=['GET'])
def get_payments(payments_id):
    """
    Retrieve a single Payment
    This endpoint will return a payment based on its id
    """
    app.logger.info('Request for payment with id: %s', payments_id)
    payment = Payment.find(payments_id)
    if not payment:
        raise NotFound(
            "Payment with id '{}' was not found.".format(payments_id))
    return make_response(jsonify(payment.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW PAYMENTS
######################################################################
@app.route('/payments', methods=['POST'])
def create_payments():
    """
    Creates a Payment
    This endpoint will create a Payment based on the body that is posted
    """
    app.logger.info('Request to create a payments')
    check_content_type('application/json')
    payment = Payment()
    request_data = request.get_json()
    jsonschema.validate(request_data, payment_schema)
    payment.deserialize(request_data)
    payment.save()
    message = payment.serialize()
    location_url = url_for('get_payments', payments_id=payment.id,
                           _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {
                             'Location': location_url
                         })


# ######################################################################
# # UPDATE AN EXISTING PAYMENT
# ######################################################################
@app.route('/payments/<int:payments_id>', methods=['PUT'])
def update_payment(payments_id):
    """
    Update a Payment
    This endpoint will update a Payment based on the body that is posted
    """
    app.logger.info('Request to update payment with id: %s', payments_id)
    check_content_type('application/json')
    payment = Payment.find(payments_id)
    if not payment:
        raise NotFound(
            "Payment with id '{}' was not found.".format(payments_id))
    request_data = request.get_json()
    jsonschema.validate(request_data, payment_schema)
    payment.deserialize(request_data)
    payment.id = payments_id
    payment.save()
    return make_response(jsonify(payment.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A PAYMENT
######################################################################
@app.route('/payments/<int:payments_id>', methods=['DELETE'])
def delete_payment(payments_id):
    """
    Delete a payment
    This endpoint will delete a Payment based on the id specified in the path
    """
    app.logger.info('Request to delete payment with id: %s', payments_id)
    payment = Payment.find(payments_id)
    if payment:
        payment.delete()
    return make_response('', status.HTTP_204_NO_CONTENT)


######################################################################
# DELETE A PAYMENT(Using for test only)
######################################################################
@app.route('/payments/reset', methods=['DELETE'])
def reset_payments():
    """ Removes all pets from the database """
    app.logger.info('Remove all the payments inside the database')
    Payment.disconnect()
    Payment.remove_all()
    return make_response('', status.HTTP_204_NO_CONTENT)


######################################################################
# PERFORM A STATEFUL ACTION
######################################################################
@app.route('/payments/<int:payments_id>/toggle', methods=['PUT'])
def toggle_payment_availability(payments_id):
    """
    Toggle payment availability
    This toggles whether or not a payment is currently available
    """
    app.logger.info('Request to toggle payment availability with id: %s',
                    payments_id)
    payment = Payment.find(payments_id)
    if not payment:
        raise NotFound(
            "Payment with id '{}' was not found.".format(payments_id))
    payment.available = not payment.available
    payment.save()
    return make_response(jsonify(payment.serialize()), status.HTTP_200_OK)


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
