# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  November 03, 2024 13:13:02
# Database: sqlite:////tmp/tmp.lcBIrx22E2/DogWalkingSystem/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Owner(SAFRSBaseX, Base):
    """
    description: Represents a dog owner who can register themselves and their pets.
    """
    __tablename__ = 'Owner'
    _s_collection_name = 'Owner'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_date = Column(Date)
    updated_date = Column(Date)
    created_by = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    DogList : Mapped[List["Dog"]] = relationship(back_populates="owner")
    WalkScheduleList : Mapped[List["WalkSchedule"]] = relationship(back_populates="owner")



class Walker(SAFRSBaseX, Base):
    """
    description: Represents a dog walker who can register and manage walk requests.
    """
    __tablename__ = 'Walker'
    _s_collection_name = 'Walker'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    max_dogs_per_walk = Column(Integer, nullable=False)
    base_price = Column(Float, nullable=False)
    availability = Column(String, nullable=False)
    created_date = Column(Date)
    updated_date = Column(Date)
    created_by = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    WalkScheduleList : Mapped[List["WalkSchedule"]] = relationship(back_populates="walker")



class Dog(SAFRSBaseX, Base):
    """
    description: Represents a dog belonging to an owner, with specific details needed for walks.
    """
    __tablename__ = 'Dog'
    _s_collection_name = 'Dog'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    owner_id = Column(ForeignKey('Owner.id'), nullable=False)
    name = Column(String, nullable=False)
    breed = Column(String)
    size = Column(String, nullable=False)
    notes = Column(String)
    created_date = Column(Date)
    updated_date = Column(Date)
    created_by = Column(String)

    # parent relationships (access parent)
    owner : Mapped["Owner"] = relationship(back_populates=("DogList"))

    # child relationships (access children)
    WalkScheduleList : Mapped[List["WalkSchedule"]] = relationship(back_populates="dog")



class WalkSchedule(SAFRSBaseX, Base):
    """
    description: Records the schedule of dog walks including matching walker with owner and dog.
    """
    __tablename__ = 'WalkSchedule'
    _s_collection_name = 'WalkSchedule'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    walker_id = Column(ForeignKey('Walker.id'), nullable=False)
    owner_id = Column(ForeignKey('Owner.id'), nullable=False)
    dog_id = Column(ForeignKey('Dog.id'), nullable=False)
    date_requested = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    created_date = Column(Date)
    updated_date = Column(Date)
    created_by = Column(String)

    # parent relationships (access parent)
    dog : Mapped["Dog"] = relationship(back_populates=("WalkScheduleList"))
    owner : Mapped["Owner"] = relationship(back_populates=("WalkScheduleList"))
    walker : Mapped["Walker"] = relationship(back_populates=("WalkScheduleList"))

    # child relationships (access children)
    PaymentList : Mapped[List["Payment"]] = relationship(back_populates="walk_schedule")



class Payment(SAFRSBaseX, Base):
    """
    description: Handles the payment details for each completed walk.
    """
    __tablename__ = 'Payment'
    _s_collection_name = 'Payment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    walk_schedule_id = Column(ForeignKey('WalkSchedule.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date_paid = Column(Date)
    created_date = Column(Date)
    updated_date = Column(Date)
    created_by = Column(String)

    # parent relationships (access parent)
    walk_schedule : Mapped["WalkSchedule"] = relationship(back_populates=("PaymentList"))

    # child relationships (access children)
