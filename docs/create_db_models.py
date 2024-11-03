# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import date   
from datetime import datetime

logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


class Walker(Base):
    """description: Represents a dog walker who can register and manage walk requests."""
    __tablename__ = 'Walker'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    max_dogs_per_walk = Column(Integer, nullable=False)
    base_price = Column(Float, nullable=False)  # base price that can vary by dog size
    availability = Column(String, nullable=False)  # e.g., 'Mon morning, Tues afternoon'
    created_date = Column(Date, default=datetime.now)
    updated_date = Column(Date, default=datetime.now, onupdate=datetime.now)
    created_by = Column(String, nullable=True)


class Owner(Base):
    """description: Represents a dog owner who can register themselves and their pets."""
    __tablename__ = 'Owner'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_date = Column(Date, default=datetime.now)
    updated_date = Column(Date, default=datetime.now, onupdate=datetime.now)
    created_by = Column(String, nullable=True)


class Dog(Base):
    """description: Represents a dog belonging to an owner, with specific details needed for walks."""
    __tablename__ = 'Dog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('Owner.id'), nullable=False)
    name = Column(String, nullable=False)
    breed = Column(String, nullable=True)
    size = Column(String, nullable=False)  # e.g., 'small', 'medium', 'large'
    notes = Column(String, nullable=True)
    created_date = Column(Date, default=datetime.now)
    updated_date = Column(Date, default=datetime.now, onupdate=datetime.now)
    created_by = Column(String, nullable=True)


class WalkSchedule(Base):
    """description: Records the schedule of dog walks including matching walker with owner and dog."""
    __tablename__ = 'WalkSchedule'

    id = Column(Integer, primary_key=True, autoincrement=True)
    walker_id = Column(Integer, ForeignKey('Walker.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('Owner.id'), nullable=False)
    dog_id = Column(Integer, ForeignKey('Dog.id'), nullable=False)
    date_requested = Column(Date, nullable=False)
    status = Column(String, nullable=False)  # e.g., 'pending', 'confirmed', 'rejected'
    created_date = Column(Date, default=datetime.now)
    updated_date = Column(Date, default=datetime.now, onupdate=datetime.now)
    created_by = Column(String, nullable=True)


class Payment(Base):
    """description: Handles the payment details for each completed walk."""
    __tablename__ = 'Payment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    walk_schedule_id = Column(Integer, ForeignKey('WalkSchedule.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date_paid = Column(Date, default=datetime.now)
    created_date = Column(Date, default=datetime.now)
    updated_date = Column(Date, default=datetime.now, onupdate=datetime.now)
    created_by = Column(String, nullable=True)


# ALS/GenAI: Create an SQLite database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# ALS/GenAI: Prepare for sample data

from datetime import date

# Test data for Walkers
walker1 = Walker(first_name='Jane', last_name='Doe', postal_code='10001', phone='555-1234', email='jane@example.com',
                 max_dogs_per_walk=3, base_price=15.0, availability='Mon morning, Wed afternoon', created_by='admin')
walker2 = Walker(first_name='John', last_name='Smith', postal_code='20002', phone='555-5678', email='john@example.com',
                 max_dogs_per_walk=2, base_price=20.0, availability='Tues morning, Thurs afternoon', created_by='admin')

# Test data for Owners
owner1 = Owner(name='Alice', address='123 Elm St', phone='555-9876', email='alice@example.com', created_by='admin')
owner2 = Owner(name='Bob', address='456 Oak St', phone='555-6543', email='bob@example.com', created_by='admin')

# Test data for Dogs
owner1_dog1 = Dog(owner_id=1, name='Rex', breed='Golden Retriever', size='large', notes='Very friendly', created_by='admin')
owner2_dog1 = Dog(owner_id=2, name='Buddy', breed='Dachshund', size='small', notes='Barks a lot', created_by='admin')

# Test data for WalkSchedules
walk_schedule1 = WalkSchedule(walker_id=1, owner_id=1, dog_id=1, date_requested=date(2023, 10, 1), status='pending', created_by='system')
walk_schedule2 = WalkSchedule(walker_id=2, owner_id=2, dog_id=2, date_requested=date(2023, 11, 2), status='confirmed', created_by='system')

# Test data for Payments
payment1 = Payment(walk_schedule_id=1, amount=15.0, created_by='billing')
payment2 = Payment(walk_schedule_id=2, amount=20.0, created_by='billing')


session.add_all([walker1, walker2, owner1, owner2, owner1_dog1, owner2_dog1, walk_schedule1, walk_schedule2, payment1, payment2])
session.commit()
