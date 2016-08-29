
from system.core.model import Model
import re

class UserModel(Model):
    def __init__(self):
        super(UserModel, self).__init__()

    def login_user(self,user_info):
        errors = []
        PASS_REGEX = re.compile('^(?=.*[a-zA-Z])') # contains characters
        if len(user_info['username']) < 3:  # checks username length
            errors.append('name and username must be at least 3 characters')
        if len(user_info['pwd']) < 4: # Checks password length
            errors.append('Password must be at least 4 characters')
        if not PASS_REGEX.match(user_info['pwd']):
            errors.append('Password must contain characters')
        if len(errors) > 0:
            return errors

        returning_user_data = {
            'username' : user_info['username'],
            'password' : user_info['pwd']
        }
        query = 'SELECT * FROM users WHERE users.username = :username LIMIT 1'
        user = self.db.query_db(query,returning_user_data)
        if len(user) == 1:
            if self.bcrypt.check_password_hash(user[0]['password'], user_info['pwd']):
                return user[0]
            else:
                errors.append('Error with username/password')
                return errors
        errors.append('login errors')
        return errors

    def register_user(self, user_info):
        errors = []
        # Do some validations Here
        PASS_REGEX = re.compile('^(?=.*[a-zA-Z])') # contains characters
        if len(user_info['name']) < 3 or len(user_info['username']) < 3:
            errors.append('name and username must be at least 3 characters')
        if len(user_info['pwd']) < 4:
            errors.append('Password must be at least 4 characters')
        if not PASS_REGEX.match(user_info['pwd']):
            errors.append('Password must contain characters')
        if len(errors) > 0:
            return errors

        pw_hash = self.bcrypt.generate_password_hash(user_info['pwd'])
        new_user_data = {
            'name' : user_info['name'],
            'username' : user_info['username'],
            'date' : user_info['date'],
            'password' : pw_hash
        }

        # FIX DATE!!!
        # query_register = 'INSERT INTO users (name, username, date, password)VALUE(:name, :username, :date, :password)'
        query_register = 'INSERT INTO users (name, username,  password)VALUE(:name, :username, :password)'

        ## Check before this to be sure its not a duplicate
        id = self.db.query_db(query_register,new_user_data)
        new_user_id = { 'id' : id }
        query_get_registered_user = 'SELECT * FROM users WHERE users.id = :id'
        registered_user = self.db.query_db(query_get_registered_user, new_user_id)
        ## check registered_user here
        return registered_user[0]

    def get_user_wishlist(self, id):
        pass
