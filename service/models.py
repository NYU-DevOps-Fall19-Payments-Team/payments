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
Models for Payment Service.

All of the models are stored in this module.

Models
------
Payment: A payment used by a customer.

Attributes
-----------
order_id (Integer): The order for which the payment was used.
customer_id (Integer): The customer associated with a payment.
available (boolean): True for payments that are available to pay.
payment_type: The type of the payment. Currently, can be credit card or Paypal.

"""
import logging
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to be initialized later in init_db().
db = SQLAlchemy()  # pylint: disable=invalid-name


class DataValidationError(Exception):
    """Used for data validation errors when deserializing."""


class Payment(db.Model):
    """
    Represents a payment.

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM).
    """

    logger = logging.getLogger('flask.app')
    app = None

    # Table Schema

    # pylint: disable=no-member

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    type = db.Column(db.String(50))
    available = db.Column(db.Boolean())
    info = db.Column(db.JSON)

    # pylint: enable=no-member

    def __repr__(self):
        return '<Payment %r>' % self.id

    def save(self):
        """Saves a payment to the data store."""
        Payment.logger.info('Saving %s', self.id)

        # pylint: disable=no-member

        if not self.id:
            db.session.add(self)
        db.session.commit()

        # pylint: enable=no-member

    def delete(self):
        """Removes a payment from the data store."""
        Payment.logger.info('Deleting %s', self.id)

        # pylint: disable=no-member

        db.session.delete(self)
        db.session.commit()

        # pylint: enable=no-member

    def serialize(self):
        """Serializes a payment into a dictionary."""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "available": self.available,
            "type": self.type,
            "info": self.info
        }

    def deserialize(self, data):
        """Deserializes a payment from a dictionary.

        Args:
            data (dict): A dictionary containing the payment data.
        """
        try:
            self.order_id = data['order_id']
            self.customer_id = data['customer_id']
            self.available = data['available']
            self.type = data['type']
            self.info = data['info']
        except KeyError as error:
            raise DataValidationError('Invalid payments: missing ' +
                                      error.args[0])
        except TypeError:
            raise DataValidationError(
                'Invalid payments: body of request contained bad or no data')
        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database session."""
        cls.logger.info('Initializing database')
        cls.app = app

        # This is where we initialize SQLAlchemy from the Flask app.
        db.init_app(app)
        app.app_context().push()

        # Make our SQLAlchemy tables.
        db.create_all()

    @classmethod
    def all(cls):
        """Returns all of the payments in the database."""
        cls.logger.info('Processing all Payments')
        return cls.query.all()

    @classmethod
    def disconnect(cls):
        """Disconnects the database."""
        db.session.remove()

    @classmethod
    def remove_all(cls):
        """Removes all documents from the database."""
        cls.logger.info('Dropping all the tables')
        db.drop_all()
        cls.logger.info('Recreating all the tables')
        db.create_all()

    @classmethod
    def find(cls, payments_id):
        """Finds a payment by its ID number.

        Args:
            payment_id (int): The payment ID number.
        """
        cls.logger.info('Processing lookup for id %s ...', payments_id)
        return cls.query.get(payments_id)

    @classmethod
    def find_by_customer(cls, customer_id):
        """Returns all of a customer's payments.

        Args:
            customer_id (int): The customer ID number.
        """
        cls.logger.info('Processing customer query for %s ...', customer_id)
        return cls.query.filter(cls.customer_id == customer_id)

    @classmethod
    def find_by_order(cls, order_id):
        """Returns all of the payments with the given order ID.

        Args:
            order_id (int): The order ID number.
        """
        cls.logger.info('Processing category query for %s ...', order_id)
        return cls.query.filter(cls.order_id == order_id)

    @classmethod
    def find_by_availability(cls, available=True):
        """Returns all available payments."""
        cls.logger.info('Processing available query for %s ...', available)
        return cls.query.filter(cls.available == available)

    @classmethod
    def find_by_type(cls, payment_type):
        """Returns all of the payments with the given type.

        Args:
            type (string): The type of the payments that you want to match.
        """
        cls.logger.info('Processing type query for %s ...', payment_type)
        return cls.query.filter(cls.type == payment_type)

    @classmethod
    def find_by(cls, customer_id, order_id, available, payment_type):
        """Find Payments using multiple filters."""
        cls.logger.info(
            'Processing query for customer_id %s, order_id %s,'
            ' available %s, type %s ...', customer_id, order_id, available,
            payment_type)
        arg_list = [customer_id, order_id, available, payment_type]
        filter_list = [
            cls.customer_id == customer_id, cls.order_id == order_id,
            cls.available == available, cls.type == payment_type
        ]
        filter_args = [
            filter_list[i] for i, val in enumerate(arg_list) if val is not None
        ]
        return cls.query.filter(*filter_args)
