# Kanban Board

## Functions

The Kanban Board can create a table of what to do in your day. It has 3 columns:
- **Do Table:** The tasks you want to do
- **Doing Table:** The tasks you are doing
- **Done Table:** The tasks you have done

The Kanban Board can:
- Add tasks to the appropriate tables
- Move tasks from one table to another
- Delete the tasks
- Users can log in, work on their schedule, and log out. The kanban board will store your data.

The basic view:
- **Demo Page:** Similar interface with the real kanban board, but to use the features, visitors have to sign up or log in. If visitors try with the buttons, they will lead them to the Sign up Page
- **Sign up Page:** where you create your account
- **Log In Page:** where you Log In to your registered account
- **Kanban Page:** where the registered users can create, change their schedule freely

## File Structure

The root directory contains the following files:

- `test.py`: Testing processes
- `requirements.txt`: The packages 
- `app.py`: Run the app

The `app` folder contains the application files:
- `__init__.py`: The configuration and initializes the app.
- `api.py`: The functions and routes to templates
- `Database.py`: The Database
- `static/` : static assets for the front end
- `templates/`: html assets for the front end
