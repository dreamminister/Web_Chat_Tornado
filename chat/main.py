from app import Application
import os.path
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.auth
import tornado.gen

def main():
    port = int(os.environ.get("PORT", 5000))
    app = Application()
    app.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':  
    main()