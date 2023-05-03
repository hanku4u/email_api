from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


# Define an Item model that inherits from declarative base class for database
class Item(Base):

    # Set the name of the database table for this model
    __tablename__ = "items"

    # Define the columns of the database table
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    description = Column(Text)
    price = Column(Integer)


class EmailType(Base):
    """
    Define a model for the email_types table.

    This model defines a table to store different types of email that users can subscribe to.
    """
    __tablename__ = "email_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)


class User(Base):
    """
    Define a model for the users table.

    This model defines a table to store information about users, including their name, email address,
    and subscription status for different types of emails.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    email = Column(String(50), unique=True, index=True)
    # add a boolean field to indicate whether or not the user is subscribed to emails
    subscribed = Column(Boolean, default=True)
    # add a relationship to the email_types table
    email_types = relationship("EmailType", secondary="user_email_types", backref="users")


class UserEmailType(Base):
    """
    Define a model for the user_email_types table.

    This model defines an association table between the users and email_types tables, with foreign keys
    to both tables as its primary key. This table will allow us to store the list of email types that
    each user is subscribed to.
    """
    __tablename__ = "user_email_types"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    email_type_id = Column(Integer, ForeignKey("email_types.id"), primary_key=True)
