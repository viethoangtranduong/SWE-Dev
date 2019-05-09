
# coding: utf-8

# In[ ]:


# import the library
from sqlalchemy import Column, String, Integer, Enum, ForeignKey, VARCHAR
from app import db


# In[ ]:


# Create the 2 table: Users and Activities table
class Users(db.Model):
    # Users Table
    # 2 attributes:
    ###  Username (VARCHAR): unique username, primary key <50 characters
    ###  Password (VARCHAR): user's password <50 characters
    
    __tablename__ = 'Users'
    Username = db.Column(db.VARCHAR(50), primary_key=True)
    Password = db.Column(db.VARCHAR(50), nullable=False)

class Activities(db.Model):
    # Activities Table
    # 4 Attributes:
    ### row_id (INT): Primary Key: unique + autoincrement
    ### Username (VARCHAR): unique username, primary key <50 characters
    ### Activity (VARCHAR): Descriptions of the task < 200 characters
    ### Status (INT): Status of the activity (1: do; 2: doing; 3: done)
    
    __tablename__ = 'Activities'
    row_id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.VARCHAR(50))
    Activity = db.Column(db.VARCHAR(200))
    Status = db.Column(db.Integer)

# Initialize database
db.create_all()
db.session.commit()

