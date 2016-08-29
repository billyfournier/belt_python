from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        self.load_model('UserModel')
        self.load_model('PokeModel')
        self.db = self._app.db

    def index(self):
        if 'user' not in session:
            return self.load_view('index.html')
        else:
            users = self.models['PokeModel'].get_other_users(session['user']['id'])
            who = self.models['PokeModel'].who_poked_me(session['user']['id'])
            count = self.models['PokeModel'].how_many_users_poked_me(session['user']['id'])['count']
            return self.load_view('pokes.html', user=session['user'], users=users, who=who, count=count)

    def logout(self):
        if 'user' in session:
            session.pop('user')
        return self.load_view('index.html')

    def login_user(self):
        for item in ['email','pwd']:
            if item not in request.form:
                flash('------- error with form -----------')
                return redirect('/')
            else:
                user_info = request.form

        user = self.models['UserModel'].login_user(user_info)
        if type(user) == list:
            for error in user:
                flash(error)
            return redirect('/')

        session['user'] = user
        return redirect('/')

    def create_user(self):
        for item in ['name','username','email','pwd','pwdc','date']:
            if item not in request.form:
                flash('error with form names')
                return redirect('/')
            else:
                user_info = request.form

        user = self.models['UserModel'].register_user(user_info)
        if type(user) == list:
            for error in user:
                flash(error)
            return redirect('/')
        session['user'] = user
        return redirect('/')
