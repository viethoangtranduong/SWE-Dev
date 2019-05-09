
# coding: utf-8

# In[1]:


import sqlalchemy as db
from sqlalchemy import create_engine, Column, Text, Integer, ForeignKey, Float, Boolean, DateTime, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import func
from sqlalchemy import Table, MetaData
import datetime
import pandas as pd
from datetime import timedelta
import numpy as np


# In[2]:

# create an engine -> will create a file database.db as our engine
engine = create_engine('sqlite:///database.db')
engine.connect()
connection = engine.connect()
metadata = MetaData()
Base = declarative_base()


# In[3]:


class Sellers(Base):

    __tablename__ = 'Sellers'
    SellerID = Column(Integer, primary_key = True)
    Firstname = Column(Text, nullable = False)
    Surname = Column(Text, nullable = False)
    Email = Column(VARCHAR(50), nullable = False)
    Phone = Column(VARCHAR(20), nullable = False)

    def __repr__(self):
        return "<Seller (ID={0}, First name={1}, Surname={2})>".format(self.SellerID, self.Firstname, self.Surname)
    
    
class Buyers(Base):
    
    __tablename__ = 'Buyers'
    BuyerID = Column(Integer, primary_key = True)
    Firstname = Column(Text, nullable = False)
    Surname = Column(Text, nullable = False)
    Email = Column(VARCHAR(50), nullable = False)
    Phone = Column(VARCHAR(20), nullable = False)

    def __repr__(self):
        return "<Buyer (ID={0}, First name={1}, Surname={2})>".format(self.BuyerID, self.Firstname, self.Surname)
    
    
class Offices(Base):
    
    __tablename__ = 'Offices'
    OfficeID = Column(Integer, primary_key = True)
    Name = Column(Text, nullable = False)
    Email = Column(VARCHAR(50), nullable = False)
    Phone = Column(VARCHAR(20), nullable = False)
    Zipcode = Column(Integer, nullable = False)

    def __repr__(self):
        return "<Office (ID={0}, Name={1}, Zipcode={2})>".format(self.BuyerID, self.Name, self.Zipcode)
    

class Agents(Base):
    
    __tablename__ = 'Agents'
    AgentID = Column(Integer, primary_key = True)
    Firstname = Column(Text, nullable = False)
    Surname = Column(Text, nullable = False)
    Email = Column(VARCHAR(50), nullable = False)
    Phone = Column(VARCHAR(20), nullable = False)

    def __repr__(self):
        return "<Agent(ID={0}, First name={1}, Surname={2})>".format(self.AgentID, self.Firstname, self.Surname)


# In[4]:


class Agents_Offices(Base):
    __tablename__ = "Agents_Offices"
    AgentID = Column(Integer, ForeignKey("Agents.AgentID"), primary_key = True)
    OfficeID = Column(Integer, ForeignKey("Offices.OfficeID"), primary_key = True)
    agent = relationship(Agents)
    office = relationship(Offices)
    
    def __repr__(self):
        return "<Agent-Offices (AgentID={0}, OfficeID={1})>".format(self.AgentID, self.OfficeID)

    
class Listings(Base):
    
    __tablename__ = 'Listings'
    ListingID = Column(Integer, primary_key = True)
    Bedroom = Column(Integer, nullable = False)
    Bathroom = Column(Integer, nullable = False)
    Price = Column(Integer, nullable = False)
    Address = Column(Text, nullable = False)
    Zipcode = Column(VARCHAR(20), nullable = False)
    DateListed = Column(DateTime, nullable = False, default = datetime.datetime.utcnow())
    ListingAgentID = Column(Integer, ForeignKey('Agents.AgentID'))
    SellerID = Column(Integer, ForeignKey('Sellers.SellerID'))
    Status = Column(Integer, nullable = False, default = 0)
    agent = relationship(Agents)
    seller = relationship(Sellers)
    

    def __repr__(self):
        return "<Listing (ListingID={0}, Bedroom={1}, Bathroom={2})>".format(self.ListingID, self.Bedroom, self.Bathroom)
    
    
class Transactions(Base):
    
    __tablename__ = 'Transactions'
    ListingID = Column(Integer, ForeignKey('Listings.ListingID'), primary_key = True)
    BuyerID = Column(Integer, ForeignKey('Buyers.BuyerID'))
    SellerID = Column(Integer, ForeignKey('Sellers.SellerID'))
    SellingAgentID = Column(Integer, ForeignKey('Agents.AgentID'))
    SellPrice = Column(Integer, nullable = False)
    DateSold = Column(DateTime, nullable = False, default = datetime.datetime.utcnow())
    listing = relationship(Listings)
    agent = relationship(Agents)
    buyer = relationship(Buyers)
    

    def __repr__(self):
        return "<Transaction(ID={0}, BuyerID={1}, SellerID={2})>".format(self.TransactionID, self.BuyerID, self.SellerID)
    

Base.metadata.create_all(engine)
# In[5]:



