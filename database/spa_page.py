import safrs
import flask_sqlalchemy
import os
import json
import subprocess

from sqlalchemy import Column, DECIMAL, DateTime, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
from safrs import jsonapi_attr, jsonapi_rpc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy import func
from typing import List
from pathlib import Path
from sqlalchemy.sql import func
from ulid import ULID
from safrs.util import classproperty
from flask import g, has_request_context, abort, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, JWTManager, get_jwt, verify_jwt_in_request
from sqlalchemy import create_engine, text
import logging 
from werkzeug.utils import secure_filename
from pathlib import Path
from sqlalchemy.dialects.sqlite import *
from config.config import Config
from .models import Base, SAFRSBaseX


class SPASection(SAFRSBaseX, Base):
    __tablename__ = 'spa_sections'
    _s_collection_name = 'SPASection'
    
    id = Column(String, primary_key=True)
    name = Column(Text, nullable=False)
    title = Column(Text)
    subtitle = Column(Text)
    label = Column(Text)
    Type = Column(Text)
    paragraph = Column(Text)
    content = Column(Text)
    #style = Column(JSON)
    background = Column(Text)
    template = Column(Text)
    order = Column(Integer, default=-1)
    hidden = Column(Boolean, default=False)
    
    page_id = Column(ForeignKey('spa_pages.id'))
    page : Mapped["SPAPage"] = relationship(back_populates=("SectionList"))


class SPAPage(SAFRSBaseX, Base):
    __tablename__ = 'spa_pages'
    _s_collection_name = 'SPAPage'
    
    id = Column(String, primary_key=True)
    name = Column(Text, nullable=False)
    contact = Column(Text, nullable=False)
    SectionList : Mapped[List["SPASection"]] = relationship(back_populates="page")

# TODO, move this to a separate file
engine = create_engine("sqlite:///" + str(Path(__file__).parent) + "/db.sqlite")
with engine.connect() as connection:
    Base.metadata.create_all(engine)
