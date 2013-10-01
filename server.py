from tornado import websocket, web, ioloop
import sqlite3 as sql
import configparser as cfgp

cfgarr = None

def main():
    global cfgarr
    cfgarr = cfgp.ConfigParser()
    cfgarr.read('taskqueue.cfg')
    app = web.Application([(r'/', IndexHandler)])
    app.listen(cfgarr['core']['port'])
    ioloop.IOLoop.instance().start()


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html", conf=cfgarr)

if __name__ == '__main__':
    main()
