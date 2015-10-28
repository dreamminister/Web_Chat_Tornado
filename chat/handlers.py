import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.auth
import tornado.gen

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = self.get_secure_cookie('username')
        if user:
            user = user.decode('utf-8')
        return user

class MainHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect('/chat')
        self.render('index.html')

class ChatHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('chat.html', user=self.current_user)

class LoginHandler(tornado.web.RequestHandler, tornado.auth.TwitterMixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("oauth_token", None):
            user = yield self.get_authenticated_user()
            self.set_secure_cookie('username', str(user['username']))
            self.redirect("/chat")
        else:
            yield self.authorize_redirect()

class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect("/")

class WebSocketHandler(BaseHandler, tornado.websocket.WebSocketHandler):
    connections = set()

    def open(self):
        WebSocketHandler.connections.add(self)

    def on_close(self):
        WebSocketHandler.connections.remove(self)

    def on_message(self, msg):
        self.send_messages(msg)

    def send_messages(self, msg):
        for conn in self.connections:
            conn.write_message({'name': self.current_user, 'msg': msg})