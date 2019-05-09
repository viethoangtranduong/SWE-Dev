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
from create import Buyers, Sellers, Offices, Agents, Agents_Offices, Listings, Transactions, connection, engine, metadata
from insert import session, engine 
import calendar
import random
from random import choice
from string import ascii_uppercase


Seller = db.Table('Sellers', metadata, autoload=True, autoload_with=engine)
Buyer = db.Table('Buyers', metadata, autoload=True, autoload_with=engine)
Office = db.Table('Offices', metadata, autoload=True, autoload_with=engine)
Agent = db.Table('Agents', metadata, autoload=True, autoload_with=engine)
Agent_Office = db.Table('Agents_Offices', metadata, autoload=True, autoload_with=engine)
Listing = db.Table('Listings', metadata, autoload=True, autoload_with=engine)
Transaction  = db.Table('Transactions', metadata, autoload=True, autoload_with=engine)

# commision function
def commission(amount):
    amount = int(amount)
    if amount < 100000:
        return 0.1*amount
    elif amount < 200000:
        return 0.075*amount
    elif amount < 500000:
        return 0.06*amount
    elif amount < 1000000:
        return 0.05*amount
    else: 
        return 0.04*amount
    
    
#1 Find the top 5 offices with the most sales for that month.
def query_office_month(number = 5, year = datetime.datetime.utcnow().year, month = datetime.datetime.utcnow().month):
    
    begin = datetime.datetime(year, month, 1)
    end = datetime.datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
    
    query = db.select([Office.columns.Name, Office.columns.Zipcode, Office.columns.Phone, 
                       db.func.sum(Transaction.columns.SellPrice).label('Total Sales'), 
                       db.func.count(Transaction.columns.SellPrice).label('Number of Sales')])\
                        .group_by(Listing.columns.Zipcode)\
                        .where(db.and_(Transaction.columns.DateSold >= begin, end >= Transaction.columns.DateSold))\
                        .order_by(db.desc(db.func.sum(Transaction.columns.SellPrice)))
                        

    query = query.select_from((Transaction.join(Listing, Transaction.columns.ListingID == Listing.columns.ListingID)).join(Office, Office.columns.Zipcode == Listing.columns.Zipcode))
    results = connection.execute(query).fetchall()[:number]
    print("Top {2} Offices with the most sales in month: {0}, year: {1}".format(month, year,number))
    if results != []:
        df = pd.DataFrame(results)
        df.columns = results[0].keys()
        print(df)
    else: 
        print("No Sales")
print("Question 1: Find the top 5 offices with the most sales for that month.")    
query_office_month()
print()
print("Additional: Find the top 2 offices with the most sales in January, 2019.")
query_office_month(2,2019,1)
print()


# In[26]:


# 2


# In[27]:

# Find the top 5 estate agents who have sold the most (include their contact details and their sales details so that it is easy contact them and congratulate them)
def top_agents(number = 5):
    query = db.select([Transaction.columns.SellingAgentID, Agent.columns.Phone, Agent.columns.Email, 
                       db.func.sum(Transaction.columns.SellPrice).label('Total Sales'), 
                       db.func.count(Transaction.columns.SellPrice).label('Number of Sales')])\
                        .group_by(Transaction.columns.SellingAgentID).order_by(db.desc(db.func.sum(Transaction.columns.SellPrice)))

    query = query.select_from(Agent.join(Transaction, 
                                         Agent.columns.AgentID == Transaction.columns.SellingAgentID))
    results = connection.execute(query).fetchall()[:number]
    df = pd.DataFrame(results)
    df.columns = results[0].keys()
    print("Top {0} agents".format(number))
    print(df)

print("Question 2: Find the top 5 estate agents who have sold the most (include their contact details and their sales details so that it is easy contact them and congratulate them).")
top_agents()
print()
print("Find the top 3 (or any numbers) estate agents who have sold the most (include their contact details and their sales details so that it is easy contact them and congratulate them).")
top_agents(3)
print()



# In[28]:


#3 


# In[32]:

# commision table
def commission_table():
    query = db.select([Transaction.columns.SellingAgentID, Agent.columns.Phone, Agent.columns.Email, Transaction.columns.SellPrice])

    query = query.select_from(Agent.join(Transaction, 
                                         Agent.columns.AgentID == Transaction.columns.SellingAgentID))
    results = connection.execute(query).fetchall()
    df = pd.DataFrame(results)
    df.columns = results[0].keys()
    df['SellPrice'] = df['SellPrice'].apply(commission)
    commission_table = df.groupby(['SellingAgentID']).sum()
    commission_table.columns = ["Total Commision"]
    commission_table.sort_values(["Total Commision"])
    print(commission_table)

print("Question 3: Calculate the commission that each estate agent must receive and store the results in a separate table.")
commission_table()
print()

# In[33]:



#4


# In[36]:
 
def average_day_on_market(year = datetime.datetime.utcnow().year, month = datetime.datetime.utcnow().month):  
    begin = datetime.datetime(year, month, 1)
    end = datetime.datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
    query = db.select([Transaction.columns.ListingID, Listing.columns.DateListed, Transaction.columns.DateSold])\
                        .where(db.and_(Transaction.columns.DateSold >= begin, end >= Transaction.columns.DateSold))

    query = query.select_from(Transaction.join(Listing, 
                                         Transaction.columns.ListingID == Listing.columns.ListingID))
    results = connection.execute(query).fetchall()
    print("Days on market of houses sold in month: {0}, year: {1}".format(month, year))
    if results != []:
        df = pd.DataFrame(results)
        df.columns = results[0].keys()
        df["On Market Day"] = abs(df["DateSold"] - df["DateListed"])
        print(pd.DataFrame(df[["ListingID", "On Market Day"]]))
        print()
        print("The average days on market of houses sold in of houses sold in month {0}, year {1}: {2} (Days) "\
              .format(month, year, np.mean(df["On Market Day"]).days + 1))
    else:
        print("No Data")

        
print("Question 4: For all houses that were sold that month, calculate the average number of days that the house was on the market.")
average_day_on_market()
print()
print("Additional: ")
average_day_on_market(month = 3)
print()

# In[37]:



# 5
def average_price(year = datetime.datetime.utcnow().year, month = datetime.datetime.utcnow().month):
    
    begin = datetime.datetime(year, month, 1)
    end = datetime.datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
    
    query = db.select([Transaction.columns.ListingID, Transaction.columns.SellPrice])\
            .where(db.and_(Transaction.columns.DateSold >= begin, end >= Transaction.columns.DateSold))

    query = query.select_from(Transaction.join(Listing, 
                                         Transaction.columns.ListingID == Listing.columns.ListingID))
    results = connection.execute(query).fetchall()
    print("The houses are sold in month: {0}, year: {1}".format(month, year))
    if results != []:
        df = pd.DataFrame(results)
        df.columns = results[0].keys()
        print(df)
        print()
        print("The average price: {0} ($)".format(int(np.mean(df["SellPrice"]))))
    else: 
        print("No Data available")
    
print("Question 5: For all houses that were sold that month, calculate the average selling price")
average_price()
print()
print("Additional For all houses that were February, 2019, calculate the average selling price")
average_price(month = 2)
print()




#6


# In[38]:


def top_zip_code(number = 5):
    
    query = db.select([Office.columns.Name, Office.columns.Zipcode, Office.columns.Phone, 
                       db.func.avg(Transaction.columns.SellPrice).label('Average Sale Price')])\
                        .group_by(Listing.columns.Zipcode).order_by(db.desc(db.func.sum(Transaction.columns.SellPrice)))

    query = query.select_from((Transaction.join(Listing, Transaction.columns.ListingID == Listing.columns.ListingID)).join(Office, Office.columns.Zipcode == Listing.columns.Zipcode))
    results = connection.execute(query).fetchall()[:number]
    if results != []:
        df = pd.DataFrame(results)
        df.columns = results[0].keys()
        print("The top {0} zipcode with highest average sale prices:".format(number))
        print(df)
    else:
        print("No Data Available")
        
print("Question 6: Find the zip codes with the top 5 average sales prices")
top_zip_code()
print()
print("Additional: Find the zip codes with the top 3 average sales prices")
top_zip_code(3)
print()