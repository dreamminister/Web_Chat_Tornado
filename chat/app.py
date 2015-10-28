import os.path
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.auth
import tornado.gen
from handlers import MainHandler, ChatHandler, LoginHandler, LogoutHandler, WebSocketHandler

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/chat', ChatHandler),
            (r'/ws', WebSocketHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
        ]
        settings = dict(
            cookie_secret="your_cookie_secret",
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            twitter_consumer_key='your_twitter_consumer_key',
            twitter_consumer_secret='your_twitter_consumer_secret',
            login_url='/',
            xsrf_cookies=True,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

