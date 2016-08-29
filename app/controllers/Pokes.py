from system.core.controller import *

class Pokes(Controller):
    def __init__(self, action):
        super(Pokes, self).__init__(action)

        self.load_model('PokeModel')
        self.db = self._app.db

    def poke_user(self, rx_id):
        tx_id = session['user']['id']
        self.models['PokeModel'].poke_user(rx_id,tx_id)
        return redirect('/')
