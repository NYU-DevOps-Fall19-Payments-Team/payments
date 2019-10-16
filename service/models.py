# Copyright 2016, 2019 John Rofrano. All Rights Reserved.
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
Models for Payment Demo Service

All of the models are stored in this module

Models
------
Payment  - A Payment used By customer

Attributes:
-----------
order_id (Integer) - the order that the payment was been used for.
customer_id (Integer) - the customer that owns the payments.
available (boolean) - True for payments that are available to pay.
payments_type - The type of the payments, so far we only support credit card.

"""
import logging
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

class Payment(db.Model):
    """
    Class that represents a Payment

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """
    logger = logging.getLogger('flask.app')
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    payments_type = db.Column(db.String(50))
    available = db.Column(db.Boolean())

    def __repr__(self):
        return '<Payment %r>' % (self.name)

    def save(self):
        """
        Saves a Payment to the data store
        """
        Payment.logger.info('Saving %s', self.id)
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Removes a Payment from the data store """
        Payment.logger.info('Deleting %s', self.id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Payment into a dictionary """
        return {"id": self.id,
                "order_id": self.order_id,
                "customer_id": self.customer_id,
                "available": self.available,
                "payments_type" : self.payments_type
                }

    def deserialize(self, data):
        """
        Deserializes a Payment from a dictionary

        Args:
            data (dict): A dictionary containing the Payment data
        """
        try:
            self.order_id = data['order_id']
            self.customer_id = data['customer_id']
            self.available = data['available']
            self.payments_type = data['payments_type']
        except KeyError as error:
            raise DataValidationError('Invalid payments: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid payments: body of request contained' \
                                      'bad or no data')
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        cls.logger.info('Initializing database')
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Payments in the database """
        cls.logger.info('Processing all Payments')
        return cls.query.all()

    @classmethod
    def find(cls, payments_id):
        """ Finds a Payment by it's ID """
        cls.logger.info('Processing lookup for id %s ...', payments_id)
        return cls.query.get(payments_id)

    # @classmethod
    # def find_or_404(cls, payments_id):
    #     """ Find a payments by it's id """
    #     cls.logger.info('Processing lookup or 404 for id %s ...', payments_id)
    #     return cls.query.get_or_404(payments_id)

    @classmethod
    def find_by_customer(cls, customer_id):
        """ Returns all the customer's payments with the given customer_id

        Args:
            id (integer): the id of customer you want to match
        """
        cls.logger.info('Processing customer query for %s ...', customer_id)
        return cls.query.filter(cls.customer_id == customer_id)

    @classmethod
    def find_by_order(cls, order_id):
        """ Returns all of the Payments in a category

        Args:
            category (string): the category of the Payments you want to match
        """
        cls.logger.info('Processing category query for %s ...', order_id)
        return cls.query.filter(cls.order_id == order_id)

    @classmethod
    def find_by_availability(cls, available=True):
        """ Query that finds Payments by their availability """
        """ Returns all Payments by their availability

        Args:
            available (boolean): True for payments that are available
        """
        cls.logger.info('Processing available query for %s ...', available)
        return cls.query.filter(cls.available == available)

    @classmethod
    def find_by_type(cls, payments_type):
        """ Query that finds Payments by their availability """
        """ Returns all Payments by their availability

        Args:
            available (boolean): True for payments that are available
        """
        cls.logger.info('Processing type query for %s ...', payments_type)
        return cls.query.filter(cls.payments_type == payments_type)
