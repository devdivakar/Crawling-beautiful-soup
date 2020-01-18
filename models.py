import os, sys, json
import pandas as pd
import numpy as np
from configuration import config
from sqlalchemy import Column, ForeignKey, Date, DateTime, UniqueConstraint, Integer, DECIMAL, VARCHAR ,TEXT,JSON,BOOLEAN,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()



class crawler_master(Base):
    __tablename__ = "crawler_master"
    id = Column(Integer, primary_key= True, autoincrement= True)
    product_name = Column(VARCHAR(length=32), nullable= False)
    crawler_site = Column(VARCHAR(length=32), nullable= False)
    client_name = Column(VARCHAR(length=32), nullable= False)
    crawler_url = Column(TEXT, nullable= False)
    crawler_config = Column(JSON)
    active = Column(BOOLEAN,default = False)


class crawler_result(Base):
    __tablename__ = "crawler_result"
    id = Column(Integer, primary_key= True, autoincrement= True)
    crawler_id = Column(VARCHAR(length=32), nullable= False)
    crawler_result = Column(JSON)
    uuid = Column(VARCHAR(length=50), nullable= False) 
    client_name = Column(VARCHAR(length=32), nullable= False)
    added_by = Column(VARCHAR(length=32), nullable= False)
    crawl_timestamp = Column(TIMESTAMP(timezone=True), nullable= False)
    crawler_site = Column(VARCHAR(length=32), nullable= False)
    product_name = Column(VARCHAR(length=32), nullable= False)
    unique_id = Column(VARCHAR(length=50),)

engine = create_engine(config["sql_url"])

Base.metadata.create_all(engine)
