
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
from create import Buyers, Sellers, Offices, Agents, Agents_Offices, Listings, Transactions, connection, engine 
import calendar
import random
from random import choice
from string import ascii_uppercase

# In[2]:
Session = sessionmaker(bind=engine)
session = Session() 
metadata = MetaData()

    
def main():
    # In[7]:

    # add random seller data
    def add_random_seller():
        FN = ''.join(choice(ascii_uppercase) for i in range(random.randint(3, 7)))
        SN = ''.join(choice(ascii_uppercase) for i in range(random.randint(3, 7)))
        Email = FN + "." + SN + "@minerva.kgi.edu"
        Phone = int(''.join(choice("0123456789") for i in range(10)))
        session.add(Sellers(Firstname = FN, Surname = SN, Email = Email, Phone = Phone))
    for i in range(100): 
        add_random_seller()
    session.commit()


        # In[8]:

    # add random buyer data
    def add_random_buyer():
        FN = ''.join(choice(ascii_uppercase) for i in range(random.randint(3, 7)))
        SN = ''.join(choice(ascii_uppercase) for i in range(random.randint(3, 7)))
        Email = FN + "." + SN + "@minerva.kgi.edu"
        Phone = int(''.join(choice("0123456789") for i in range(10)))
        session.add(Buyers(Firstname = FN, Surname = SN, Email = Email, Phone = Phone))

    for i in range(100): 
        add_random_buyer()

    session.commit()


        # In[10]:

    # add random office data
    def add_random_office(Zipcode):
        Name = ''.join(choice(ascii_uppercase) for i in range(5))
        Email = Name + "_" + str(Zipcode) + "@minerva.kgi.edu"
        Phone = int(''.join(choice("0123456789") for i in range(10)))
        session.add(Offices(Name = Name, Email = Email, Phone = Phone, Zipcode = Zipcode))

    for Zipcode in range(94100, 94121): 
        add_random_office(Zipcode)

    session.commit()
    session.commit()


        # In[12]:

    # add random agent data
    def add_random_agent():
        FN = ''.join(choice(ascii_uppercase) for i in range(random.randint(3, 7)))
        SN = ''.join(choice(ascii_uppercase) for i in range(random.randint(3, 7)))
        Email = FN + "." + SN + "@minerva.kgi.edu"
        Phone = int(''.join(choice("0123456789") for i in range(10)))
        session.add(Agents(Firstname = FN, Surname = SN, Email = Email, Phone = Phone))

    for i in range(50): 
        add_random_agent()

    session.commit()

        # In[14]:

    # add random office-agent relation data
    def random_office_agent(AgentID):
        population = set(range(1,21))
        relations  = random.randint(1, 10)
        samples = random.sample(population, relations)
        for i in samples:
            session.add(Agents_Offices(AgentID = AgentID, OfficeID = i))

    for AgentID in range(50):
        random_office_agent(AgentID)
    session.commit()


        # In[16]:




        # In[17]:

    # Add new house
    def add_listing():
        BeR = random.randint(1,7)
        BaR = random.randint(1,7)
        Pri = random.randint(100000, 1000000)
        Add = ''.join(choice(ascii_uppercase) for i in range(random.randint(20, 40)))
        Zip = random.randint(94100, 94120)
        Dat = datetime.datetime(random.randint(2017, 2019), random.randint(1,12), random.randint(1,28))
        AID = random.randint(1, 50)
        SID = random.randint(1, 100)
        session.add(Listings(Bedroom = BeR, Bathroom = BaR, Price = Pri, Address = Add, Zipcode = Zip, DateListed = Dat, ListingAgentID = AID, SellerID = SID, Status = 0))

    for i in range(200):
        add_listing()
    session.commit()


    # In[18]:


    # In[19]:


    # In[20]:
    # As a transaction requires checking the conditions and multiple update, I did a function to capture this
    def buy_process(BuyerID, ListingID, SellingAgentID, SellPrice):
        buyer = session.query(Buyers).filter(Buyers.BuyerID==BuyerID).first()
        house = session.query(Listings).filter(Listings.ListingID==ListingID).first()
        if buyer == None:
            print("Invalid BuyerID")
        elif house == None:
            print("Invalid HouseID")
        elif house.Status == 1:
            print("Cannot make transactions! House has been SOLD!")
        else: 
            house.Status = 1

            transaction = Transactions(ListingID = house.ListingID,
                                       BuyerID = buyer.BuyerID,
                                       SellerID = house.SellerID,
                                       SellingAgentID = SellingAgentID,
                                       SellPrice = SellPrice)

            session.add(transaction)
            session.commit()
            
            
    population = set(range(1,101))
    samples = random.sample(population, 50)
    for i in samples:
        buy_process(random.randint(1, 100), i, random.randint(1, 50), random.randint(100000, 1000000))


    # In[21]:




    # In[22]:


    
    
    session.commit()

    
    
if __name__ == "__main__":
    main()

