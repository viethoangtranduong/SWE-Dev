
# coding: utf-8

# In[ ]:


### Import important library
### import Database.py for storing users' data
### sqlite3 as the primary database
from app import db, app
import hashlib
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, g
from .Database import Users, Activities
import sqlite3


# In[ ]:


# Hash the users password
def hash_password(users_password): 
    # input: user password
    # then encode to convert into bytes
    return hashlib.sha256(users_password.encode()).hexdigest()


# ### Templates Structure

# #### Login Page

# In[ ]:


@app.route('/login')
def log_in():
    # Go to login template
    return render_template('login.html')


# #### Sign Up Page

# In[ ]:


@app.route('/signup')
def sign_up():
    # Go to sign up template
    return render_template('signup.html')


# #### Log Out Page

# In[ ]:


@app.route('/logout')
def log_out():
    # Pop the Username out of the current session
    session.pop('Username', None)
    # show message
    flash('You were logged out!')
    # go back to the front page
    return redirect(url_for('check_session'))


# #### Demo Page
# This is the View Page for any visitors. The demo version allows visitors to see the UI of the inside, but does not allow them to use any feature. They will have to sign in to be able to use the features. Also, if the try to click to use the feature, the page will redirect them to the log in page

# In[ ]:


@app.route('/demo')
# let the user try out the product before signing up
def demo():
    return render_template('demo.html')


# #### User's Kanban Board Page

# In[ ]:


@app.route('/kanban')
def kanban():
    # Go to kanban template
    return render_template('kanban.html')


# ### Functions

# #### Sign Up Process

# In[ ]:


@app.route('/signup', methods=["POST"])
def sign_up_process():
    # Check if the user exists
    current_user = db.session.query(Users).filter(Users.Username==request.form['Username']).first()
    # If the username is existed already -> invalid -> refresh
    if current_user != None:
        flash('Existed Username!')
        return render_template('signup.html')
    
    # If the username is available -> sign up successfully
    else:
        current_user = Users(
            Username = request.form['Username'],
            Password = hash_password(request.form['Password'])
        )
        
        # Add the user into the database, commit and redirect to login
        db.session.add(current_user)
        db.session.commit()
        flash('Registered successfully. Try Logging in to continue!')
        return redirect(url_for('log_in'))


# #### Log In Process

# In[ ]:


@app.route('/login', methods=['POST'])
def log_in_process():
    
    # Take input
    current_user = db.session.query(Users).filter(Users.Username==request.form['Username']).first()
    current_password = hash_password(request.form['Password'])

    # Check if username is in database. If not -> invalid
    # refresh 
    if current_user == None or current_password != current_user.Password:
        flash('Invalid username or password')
        return redirect(url_for('log_in_process'))
    # If username is in the database, then check password.
    # If the password matches, then log in
    else:
        session['Username'] = current_user.Username
        flash('Log in successfully!')
        return redirect(url_for('check_session'))


# #### Check current session

# In[ ]:


@app.route('/')
def check_session():
    
    # check if there is any user is using the system
    result = session.get("Username")
    
    # If the visitor is not currently sign in
    # allow them to see the demo view
    if result == None: 
        return redirect(url_for('demo'))
    
    # If the visitor is signed in
    # query back to the user's history to display the tasks they inserted
    else:
        activities = db.session.query(Activities).filter(Activities.Username==session.get('Username'))
        # empty lists for displaying
        do = []
        doing = []
        done = []
        
        # check with activity belongs to which section: do - doing - done
        for act in activities:
            if act.Status == 1:
                do.append(act)
            elif act.Status == 2:
                doing.append(act)
            elif act.Status == 3:
                done.append(act)
                
    # display the template with the given information
    return render_template('kanban.html', 
                           do = do, 
                           doing = doing, 
                           done = done, 
                           user = session.get('Username'))


# ### Kanban Board Tasks

# #### Add

# In[ ]:


# Add
@app.route('/add', methods=['POST'])
def add_task():
    
    # If the visitor is not logged in yet, redirect to log in page
    if session.get("Username") == None:
        flash("This feature is for registered users only")
        flash("Redirecting you to Log in page")
        return redirect(url_for('log_in'))
    
    # If the user is logged in
    # If the request form is from the "do" section
    ### add the activity to Status 1: do
    if request.form['do'] != None: 
        act = Activities(
            Username = str(session.get('Username')),
            Activity = str(request.form['do']),
            Status = 1)
    # If the request form is from the "doing" section
    ### add the activity to Status 2: doing
    elif request.form['doing'] != None: 
        act = Activities(
            Username = session.get('Username'),
            Activity = request.form['doing'],
            Status = 2)
    # Else: Means that the request form is from the "done" section
    ### add the activity to Status 3: done
    else:
        act = Activities(
            Username = session.get('Username'),
            Activity = request.form['done'],
            Status = 3)
        
    # Add to the session and database
    db.session.add(act)
    db.session.commit()
    
    # reload the page
    return redirect(url_for('check_session'))


# #### Move tasks

# In[ ]:


@app.route('/movetask/<row_id>/<new_Status>')
def move_task(row_id , new_Status):
    
    new_Status = int(new_Status)
    
    # If the visitor is not logged in yet, redirect to log in page
    if session.get("Username") == None:
        flash("This feature is for registered users only")
        return redirect(url_for('log_in'))
    
    # Check the activity with the given row_id
    act = db.session.query(Activities).filter(Activities.row_id == int(row_id)).first()
    
    # If the task does not exist, abort
    if act == None:
        flash("Invalid action!")
        abort(404)
        
    # Else, update the status with the new_Status
    # commit and refresh page
    act.Status = new_Status
    db.session.commit()  
    return redirect(url_for('check_session'))


# #### Delete tasks

# In[ ]:


@app.route('/delete/<row_id>', methods=['GET', 'POST', 'DELETE'])
def delete_task(row_id):
    # Need to be logged in to change the status of task
    if session.get("Username") == None:
        flash("This feature is for registered users only")
        return redirect(url_for('log_in'))
        
    act = db.session.query(Activities).filter(Activities.row_id==int(row_id)).first()
    # If the task does not exist, abort
    if act == None:
        flash("Invalid action!")
        abort(404)
        
    # Else, delete the status from database
    db.session.delete(act)
    db.session.commit()
    return redirect(url_for('check_session'))


# ### Run

# In[ ]:


if __name__ == '__main__':
    app.run(debug=True)

