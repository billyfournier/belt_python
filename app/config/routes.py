from system.core.router import routes

routes['default_controller'] = 'Users'
routes['POST']['/users/register'] = 'Users#create_user'
routes['POST']['/users/login'] = 'Users#login_user'
routes['/users/logout'] = 'Users#logout'

routes['/pokes/poke/<rx_id>'] = 'Pokes#poke_user'
