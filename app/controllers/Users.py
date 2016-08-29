from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        self.load_model('UserModel')
        self.db = self._app.db

    def index(self):
        if 'user' not in session:
            return self.load_view('index.html')
        else:
            wishlist = self.models['WishlistModel'].get_user_wishlist_items(session['user']['id'])
            otherlist = self.models['WishlistModel'].get_other_wishlist_items(session['user']['id'])
            return self.load_view('dashboard.html', user=session['user'], wishlist=wishlist, otherlist=otherlist )

    def logout(self):
        session.pop('user')
        return self.load_view('index.html')

    def login(self):
        for item in ['username','pwd']:
            if item not in request.form:
                print '------- error with form -----------'
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

    def register(self):
        for item in ['name','username','pwd','pwdc','date']:
            if item not in request.form:
                print '------- error with form -----------'
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
