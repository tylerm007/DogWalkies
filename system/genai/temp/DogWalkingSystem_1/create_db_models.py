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
    """description: Table for storing registered dog walkers."""
    __tablename__ = 'walker'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    max_dogs_per_walk = Column(Integer)
    price_per_walk = Column(Float)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    created_by = Column(String)



class Owner(Base):
    """description: Table for storing registered dog owners."""
    __tablename__ = 'owner'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    created_by = Column(String)



class Dog(Base):
    """description: Table for storing registered dogs for owners."""
    __tablename__ = 'dog'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('owner.id'))
    name = Column(String, nullable=False)
    breed = Column(String)
    size = Column(String, nullable=False)  # [small, medium, large]
    notes = Column(String)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    created_by = Column(String)



class WalkSchedule(Base):
    """description: Table for scheduling and tracking dog walks."""
    __tablename__ = 'walk_schedule'

    id = Column(Integer, primary_key=True)
    walker_id = Column(Integer, ForeignKey('walker.id'))
    owner_id = Column(Integer, ForeignKey('owner.id'))
    date = Column(Date)
    time = Column(String)  # [morning, afternoon]
    status = Column(String)  # [requested, confirmed, rejected]
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    created_by = Column(String)



class Payment(Base):
    """description: Table for managing payments from owners to walkers."""
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True)
    walk_schedule_id = Column(Integer, ForeignKey('walk_schedule.id'))
    owner_id = Column(Integer, ForeignKey('owner.id'))
    walker_id = Column(Integer, ForeignKey('walker.id'))
    amount = Column(Float)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    created_by = Column(String)



# ALS/GenAI: Create an SQLite database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# ALS/GenAI: Prepare for sample data

import datetime

# Walker objects
walker1 = Walker(first_name='John', last_name='Doe', postal_code='12345', phone='123-456-7890',
                 email='john@example.com', max_dogs_per_walk=3, price_per_walk=15,
                 created_date=datetime(2023, 10, 1), updated_date=datetime(2023, 10, 2), created_by='system')
walker2 = Walker(first_name='Jane', last_name='Smith', postal_code='54321', phone='987-654-3210',
                 email='jane@example.com', max_dogs_per_walk=2, price_per_walk=20,
                 created_date=datetime(2023, 10, 1), updated_date=datetime(2023, 10, 2), created_by='system')

# Owner objects
owner1 = Owner(name='Alice Cooper', address='456 Elm St', phone='555-123-4567',
               email='alice@example.com',
               created_date=datetime(2023, 10, 3), updated_date=datetime(2023, 10, 4), created_by='system')
owner2 = Owner(name='Bob Marley', address='789 Oak Ave', phone='555-987-6543',
               email='bob@example.com',
               created_date=datetime(2023, 10, 3), updated_date=datetime(2023, 10, 4), created_by='system')

# Dog objects
# Linking to owner1

dog1 = Dog(owner_id=owner1.id, name='Rex', breed='Golden Retriever', size='large', notes='Loves to play fetch',
           created_date=datetime(2023, 10, 5), updated_date=datetime(2023, 10, 6), created_by='system')
dog2 = Dog(owner_id=owner1.id, name='Buddy', breed='Bulldog', size='medium', notes='Very friendly',
           created_date=datetime(2023, 10, 5), updated_date=datetime(2023, 10, 6), created_by='system')

# Linking to owner2

dog3 = Dog(owner_id=owner2.id, name='Max', breed='Beagle', size='small', notes='Great with kids',
           created_date=datetime(2023, 10, 5), updated_date=datetime(2023, 10, 6), created_by='system')
dog4 = Dog(owner_id=owner2.id, name='Bella', breed='Poodle', size='large', notes='Very energetic',
           created_date=datetime(2023, 10, 5), updated_date=datetime(2023, 10, 6), created_by='system')

# WalkSchedule objects
schedule1 = WalkSchedule(walker_id=walker1.id, owner_id=owner1.id, date=date(2023, 10, 10),
                         time='morning', status='requested',
                         created_date=datetime(2023, 10, 7), updated_date=datetime(2023, 10, 8), created_by='system')
schedule2 = WalkSchedule(walker_id=walker2.id, owner_id=owner1.id, date=date(2023, 10, 11),
                         time='afternoon', status='confirmed',
                         created_date=datetime(2023, 10, 7), updated_date=datetime(2023, 10, 8), created_by='system')

# Payment objects
payment1 = Payment(walk_schedule_id=schedule1.id, owner_id=owner1.id, walker_id=walker1.id, amount=15.00,
                   created_date=datetime(2023, 10, 9), updated_date=datetime(2023, 10, 10), created_by='system')
payment2 = Payment(walk_schedule_id=schedule2.id, owner_id=owner1.id, walker_id=walker2.id, amount=20.00,
                   created_date=datetime(2023, 10, 9), updated_date=datetime(2023, 10, 10), created_by='system')



session.add_all([walker1, walker2, owner1, owner2, dog1, dog2, dog3, dog4, schedule1, schedule2, payment1, payment2])
session.commit()
