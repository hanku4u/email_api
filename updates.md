# Items updated at home

## pip install passlib
-passlib[bcrypt]

## sqlite3 editor extension
- allows for read and write to sqlite in vscode

## pip install pip install python-jose
- pip install python-jose[cryptography]
- this is for generating JWT tokens

## admin_router
- added admin router with endpoint to login

## oauth2.py
- added file to handle creating access token. Some of the stuff here will go into .env
- function to verify access token is valid
- function to get current user and verify access token (using function above) at same time

## utils.py
- added utilities file
- added hash function to hash passwords
- added verify function that will verify hashed pw against hashed pw in the DB
- put the get_db function here

## models.py
- add user_roles table
- add hashed password column to users. this will be a default for everyone except admins
- add column (relationship) to user table that identifies the users roles.

## schemas.users.py
- update user model and table to add exrtra columns
- added class for UserLogin
- added schema for access token and token data (i.e. user fields encrypted into the token)

## overall note
- add a dependency to a route like this:
```python
@user_router.put("/update_user/{user_id}", response_model=schemas.User)
    def update_user_by_id(
        user_update: schemas.UserUpdate,
        user_id: int,
        current_user: int = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db),
        ):
```
- you will have to pass the access token in the request as well. Use postman for that. will not work in swagger docs
- add this to endpoints to check if user_id passed to route is the same as the user_id verfied by the token:
```python
    # check user_id from token matches user_id passed
    if current_user != user_id:
        # log failure
        logger.error(f'Endpoint: /update_user, User ID:{user_id}, Method: GET, Status: Failed, ID not found')
        raise HTTPException(status_code=404, detail="wrong user ID")
```

## TODOs
- implement token for all users. give a default password to all the users when DB is built
- force user to change password on login with default password
- subscribe users to emails based on titles
- scripts to recreate the emails themselves
- static HTML files for emails using jinja
- implement background tasks
- backup DB once a day. should be able to just write a copy to the S3 bucket.
- update users table periodically. need to get just active users and then look for any users that have
gone inactive or new users.
- add email lists (i.e. a group of emails that are for all supervisors, or a group of emails that 
all TR's should receive ect...)