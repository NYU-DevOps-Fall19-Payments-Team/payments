from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost:3306/payments"
db = SQLAlchemy(app)

class Payments(db.Model):
    """
    Class that represents a Payments
    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """
    logger = logging.getLogger('flask.app')
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    types = db.Column(db.String(63))
    available = db.Column(db.Boolean())

    def __repr__(self):
        return '<Payments %r>' % (self.name)

    def save(self):
        """
        Saves a Payments to the data store
        """
        Payments.logger.info('Saving %s', self.types)
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Removes a Payments from the data store """
        Payments.logger.info('Deleting %s', self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Payments into a dictionary """
        return {"id": self.id,
                "types": self.types,
                "available": self.available}

    def deserialize(self, data):
        """
        Deserializes a Payments from a dictionary
        Args:
            data (dict): A dictionary containing the Payments data
        """
        self.types = data['types']
        self.available = data['available']
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
        cls.logger.info('Processing all Pets')
        return cls.query.all()

@app.route('/')
def index():
    return "Hello Flask"

if __name__ == "__main__":
    Payments.init_db(app)
    dummyPayment = {
        "types":"credit card",
        "available": True
    }
    payment = Payments()
    payment.deserialize(dummyPayment)
    payment.save()
    app.run()
