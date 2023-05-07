# Items updated at home

## pip install passlib
-passlib[bcrypt]

## pip install pip install python-jose
- pip install python-jose[cryptography]
- this is for generating JWT tokens

## admin_router
- added admin router with endpoint to login
- 

## utils.py
- added utilities file
- added hash function to hash passwords
- added verify function that will verify hashed pw against hashed pw in the DB
- put the get_db function here

## models.py
- add user_roles table
- add hashed password column to users. this will be a default for everyone except admins
- add column (relationship) to user table that identifies the users roles.

## users.py
- update user model and table to add exrtra columns
- added class for UserLogin