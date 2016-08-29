
from system.core.model import Model
import re

class UserModel(Model):
    def __init__(self):
        super(UserModel, self).__init__()

    def login_user(self,user_info):
        errors = []

        if len(user_info['email']) < 1:
            errors.append('must provide an email')
            if len(user_info['pwd']) < 1:
                errors.append('must provide a password')
        if len(errors) > 0:
            return errors

        returning_user_data = {
            'email' : user_info['email'],
            'password' : user_info['pwd']
        }
        query = 'SELECT * FROM users WHERE users.email = :email LIMIT 1'
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
        if len(user_info['name']) < 3:
            errors.append('name and username must be at least 3 characters')
        if len(user_info['username']) < 3:
            errors.append('name and username must be at least 3 characters')
        PASS_REGEX = re.compile('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
        if not PASS_REGEX.match(user_info['pwd']):
            errors.append('Password must contain a number and be a minimum of 8 characters')
        EMAIL_REGEX = re.compile('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$')
        if not EMAIL_REGEX.match(user_info['email']):
            errors.append('Must provide a valid email address')
        if user_info['pwd'] != user_info['pwdc']:
            errors.append('passwords must match')
        if len(errors) > 0:
            return errors

        pw_hash = self.bcrypt.generate_password_hash(user_info['pwd'])
        new_user_data = {
            'name' : user_info['name'],
            'alias' : user_info['username'],
            'email' : user_info['email'],
            'password' : pw_hash
        }
        query_check = 'SELECT * FROM users WHERE users.email = :email '
        check = self.db.query_db(query_check, new_user_data)
        if len(check) != 0:
            errors.append('This email already exists')
            return errors
        query_register = 'INSERT INTO users (name, alias, email, password)VALUE(:name, :alias, :email, :password)'

        ## Check before this to be sure its not a duplicate
        id = self.db.query_db(query_register,new_user_data)
        new_user_id = { 'id' : id }
        query_get_registered_user = 'SELECT * FROM users WHERE users.id = :id'
        registered_user = self.db.query_db(query_get_registered_user, new_user_id)
        ## check registered_user here
        return registered_user[0]
