Components: files: 
1. `README.md` :The description of the database and files
2. `requirements.txt`: The file contains the neccessary packages for successfully running the codes
3. `create.py`: The file to create the Database with SQLAlchemy
4. `insert.py`: The file to insert data into the tables
5. `query.py`: The file to query the needed information. When this file runs, we will see the resulted tables, numbers with suitable caption.


How to run the code: 
- Create Virtual Environment: `$ virtualenv venv `
- Activate the enviroment `$ venv/Scripts/activate `
- Install required packages `pip install -r requirements.txt`
- Run the `create.py` file to create Database: `python create.py`
- Run the `create.py` file to insert data into the Database: `python insert.py`
- Run the `create.py` file to query from the Database: `python query.py`



There are 7 tables:
1. Buyers: All the contact information of the buyers and a unique BuyerID for each buyer
2. Sellers: All the contact information of the sellers and a unique SellerID for each seller
3. Office: All the office information and a unique OfficeID for each Office
4. Agents: All the agents information and a unique AgentID for each agent
5. Agents_Offices: This table demonstrate the many-to-many relationship between Office and Agents: One Office can have many Agents and One Agent can work for many Offices. This table is built upon the OfficeID and AgentID: the ForeignKey from table Agents and Offices
6. Listings: All the required information about the house, with a unique ListingID of each house. This table has 2 ForeignKeys, which are SellerID and ListingAgentID from Sellers table and Listings table.
7. Transactions: All the required information needed for a transaction: Buyers, Sellers, Selling Agents, and the ListingID, all are ForeignKeys.



The roll of DateTime: There are DateListed and DateSold variables in the above tables. The default of these variables in the immediate datetime when recorded in UTC: by using the package datetime. The function is datetime.datetime.utcnow()



A few reasonings for the design of the table:
1. The tables are guaranteed to be in first normalization form: where all the entries are atomic and no repeating groups exist (i.e. the Agents-Offices table helps to fix the complexity of many-to-many relationship, making no repeating groups occur)
2. The tables are guaranteed to be in second normalization form: it is already in first normal form and all non-key attributes are fully functional dependent on the primary key: Every table except the Agents_Offices table only contains 1 primary key, which mean it's automatically in the 2nd form. The Agents_Offices table has no non-key attributes, hence, all non-key attributes are fully functional dependent on the primary keys.  
3. The tables are guaranteed to be in the third normalization form: it is already in the 2nd form and there is no transitive functional dependency. (i.e. The major possible issue is the commission, as if we include the commission in the Transactions table, we will have the price depends on the ListingID, and the commision depends on the price -> the commision is transitively dependent on the ListingID via the price. We have resolve this by creating a function outside and only calculate when needed. <br>  However, we must be conscious that if the commission formula changed, we need to modify the comission functions and include the filter: if we change the policy after 2019/01/01: <br>
`if querying the date of the transaction < datetime.datetime(2019,1,1):
      implement former commission formula
else:
      implement the new commission formula`
4. I created functions to flexibly and conviniently accomplish the insertion and query. Among those, the insertion for transaction is more complex: we need to modify the Listings Table to change the house's status from Available (0) to Sold (1). Also, we need to check if the house were sold or not. Hence, I created a full function to account for all those behaviors and possible logically error. In this function, when a transaction is made, the Listing Table will be modified as well. We modify the status of the house instead of deleting because it's more flexible for us to access the data and better maintainance the database. After finish ever steps, then we commit the session: to guarantee all components are successfully ran.  -> sufficient length for a transaction.



The functions description: These functions allow querying flexibly, demanding on the demand (number of query agents, from which date, etc.). These functions allow query effectively, without constructing the querying syntax everytime. Furthermore, these functions account for no data output, with the print statement `No Data available`:
1. `query_office_month(x,y,z)` takes 3 optional inputs to query the top `<x>` offices those have the highest sales in month `<z>`, year `<y>`. The default for  `<x>` is 5, the default for the month and year os the cuurent month and year in UTC time.
2. `top_agents(x)` takes 1 optional input to represent the top `<x>` agents with highest sales ever
3. `commission_table()` calculate the total commission of each agents by summing up the commissions of separate transaction.
4. `average_price(y,z)` takes 2 optional input to query the average SellPrice of the selected month and year, given by `<y>`: year, and `<z>`: month
5. `average_day_on_market(x,y)` calculate the average listing day by taking the DateSold minus the DateListed. The result is round up to the nearest days. `<x>` is the year and `<y>` is the month.
6. `top_zip_code(x)` query the `<x>` number of zipcode with highest average price. The default is querying 5 zipcodes.



The assumption: 
- Each Office covers 1 zipcode only. Hence, if the Office is responsible of a given Listing means that the House's zipcode = Office's zipcode
- Each month starts from 00:00:00 of the 1st day and ends at 23:59:59 of the last day of the month (using `calendar.monthrange()` function)


There are also functions to add random data into the database. 

Source: 
- SQLAlchemy. (n.d.). SQLAlchemy 1.3 Documentation. Retrieved from https://docs.sqlalchemy.org/en/latest/orm/query.html
- Toward Data Science. (2018, August 23). SQLAlchemy - Python Tutorial. Retrieved from https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91