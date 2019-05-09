
# coding: utf-8

# In[ ]:


import os
from app import db
import app
import unittest
import tempfile
import hashlib
from app.Database import Users, Activities


# In[ ]:


# Create a Tests Class

class Tests(unittest.TestCase):
    def setUp(self):
        # Creates a new test client and initializes a new database
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        # Closes the test database
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])
        
    def test_signup(self):
        # Create an account with Username = "Test" and Password = "CS162"
        self.app.post('/signup', 
                      data = dict(Username = "Test",
                                  Password = "CS162"),
                      follow_redirects = True)
        
        # Get User's data through the Username
        User = db.session.query(Users).filter(Users.Username == "Test").first()
        
        # check the password is it matches the database
        self.assertTrue(hashlib.sha256("CS162".encode()).hexdigest() == User.Password)   
    
    # sign up testing
    def test_signin(self):
        # Create an account with Username = "Test" and Password = "CS162"
        self.app.post('/signup', 
                      data = dict(Username = "Test",
                                  Password = "CS162"),
                      follow_redirects = True)
        
        # Get User's data through the Username
        User = db.session.query(Users).filter(Users.Username=='Test').first()
        
        # Log in
        result = self.app.post('/login', data=dict(
            Username="Test",
            Password= "CS162"
        ), follow_redirects=True)
        
        # Check the flash response
        assert b"Log in successfully!" in result.data
        
    # sign out test    
    def test_signout(self):
        # Create an account with Username = "Test" and Password = "CS162"
        self.app.post('/signup', 
                      data = dict(Username = "Test",
                                  Password = "CS162"),
                      follow_redirects = True)
        
        # Get User's data through the Username
        User = db.session.query(Users).filter(Users.Username=='Test').first()
        
        # Log in
        self.app.post('/login', data=dict(Username="Test",
                                          Password= "CS162"),
                      follow_redirects=True)
        
        # Try logging out
        result = self.app.get('/logout',
                      follow_redirects=True)
        assert b"You were logged out!" in result.data
        
    # add task test    
    def test_addtask(self):
        # Create an account with Username = "Test" and Password = "CS162"
        self.app.post('/signup', 
                      data = dict(Username = "Test",
                                  Password = "CS162"),
                      follow_redirects = True)
        
        # Get User's data through the Username
        User = db.session.query(Users).filter(Users.Username=='Test').first()
        
        # Log in
        self.app.post('/login', data=dict(Username="Test",
                                          Password= "CS162"),
                      follow_redirects=True) 
        
        # Try adding the task "Testing" 
        self.app.post('/add', 
                      data = dict(Username = "Test",
                                  do = "Testing"),
                      follow_redirects = True)
        
        # query the action 
        act = db.session.query(Activities).filter(Activities.Activity=='Testing').first()
        
        # checking the Status to see if it's inserted or not
        assert act.Status == 1
     
    # move task test
    def test_movetask(self):
        # Create an account with Username = "Test" and Password = "CS162"
        self.app.post('/signup', 
                      data = dict(Username = "Test",
                                  Password = "CS162"),
                      follow_redirects = True)
        
        # Get User's data through the Username
        User = db.session.query(Users).filter(Users.Username=='Test').first()
        
        # Log in
        self.app.post('/login', data=dict(Username="Test",
                                          Password= "CS162"),
                      follow_redirects=True) 
        
        # Try adding the task "Testing"
        self.app.post('/add', 
                      data = dict(Username = "Test",
                                  do = "Testing"),
                      follow_redirects = True)
        
        # query the action
        act = db.session.query(Activities).filter(Activities.Activity=='Testing').first()
        
        # move the task from "do" section to "doing" section
        self.app.get('/movetask/'+str(act.row_id)+'/2', data=dict(
            row_id =act.row_id,
            new_Status = 2
        ), follow_redirects=True)
        
        # query the action
        act = db.session.query(Activities).filter(Activities.Activity=='Testing').first()
        
        # Checking the Status to check if it's moved yet
        assert act.Status == 2
        
    
    # delete task test
    def test_deletetask(self):
        # Create an account with Username = "Test" and Password = "CS162"
        self.app.post('/signup', 
                      data = dict(Username = "Test",
                                  Password = "CS162"),
                      follow_redirects = True)
        
        # Get User's data through the Username
        User = db.session.query(Users).filter(Users.Username=='Test').first()
        
        # Log in
        self.app.post('/login', data=dict(Username="Test",
                                          Password= "CS162"),
                      follow_redirects=True) 
        
        # Try adding the task "Testing"
        self.app.post('/add', 
                      data = dict(Username = "Test",
                                  do = "Testing"),
                      follow_redirects = True)
        
        # query the action
        act = db.session.query(Activities).filter(Activities.Activity=='Testing').first()
        
        # delete the task
        self.app.get('/delete/'+str(act.row_id), data=dict(
            row_id = act.row_id) ,follow_redirects = True)
        
        # query the task again
        act = db.session.query(Activities).filter(Activities.row_id==act.row_id).first()
        
        # check if it's deleted or not
        assert act == None
        

# Run the program
if __name__ == '__main__':
    unittest.main()

