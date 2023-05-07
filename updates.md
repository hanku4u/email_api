# Items updated at home

## pip install passlib
-passlib[bcrypt]

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
- @user_router.put("/update_user/{user_id}", response_model=schemas.User)
    def update_user_by_id(
        user_update: schemas.UserUpdate,
        user_id: int,
        current_user: int = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db),
        ):
- you will have to pass the access token in the request as well. User postman for that. will not work in swagger docs