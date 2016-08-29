
from system.core.model import Model
import re

class PokeModel(Model):
    def __init__(self):
        super(PokeModel, self).__init__()


    def poke_user(self,rx_id, tx_id):
        data = {
            'rx_id': rx_id,
            'tx_id': tx_id
        }
        query = 'INSERT INTO pokes (users_rx_id, users_tx_id)VALUE(:rx_id, :tx_id)'
        self.db.query_db(query,data)
        return True

    def who_poked_me(self, user_id):
        #order by # of times they poked me
        print user_id, '8'* 40
        query =  'SELECT users.alias, COUNT(users.alias) as poke_count from pokes '
        query += 'JOIN users on users.id = pokes.users_tx_id '
        query += 'WHERE pokes.users_rx_id = :id '
        query += 'GROUP BY users.alias '
        query += 'ORDER by poke_count DESC'
        who_poked_me = self.db.query_db(query, { 'id': user_id })
        return who_poked_me

    def get_other_users(self, my_id):
        query =  'SELECT users.*, count(pokes.users_rx_id) as num_poke FROM users '
        query += 'LEFT JOIN pokes ON users.id = pokes.users_rx_id '
        query += 'WHERE users.id != :id '
        query += 'GROUP BY users.alias'

        users = self.db.query_db(query, { 'id' : my_id })
        return users


    def how_many_users_poked_me(self, user_id):
        query =  'SELECT COUNT(DISTINCT(users.alias)) AS count FROM pokes '
        query += 'JOIN users ON pokes.users_tx_id = users.id '
        query += 'WHERE pokes.users_rx_id = :id'
        count = self.db.query_db(query, { 'id':user_id })
        return count[0]
