#!/usr/bin/env python3
from tornado import websocket, web, ioloop
#import sqlite3 as sql
import configparser as cfgp
import utils
import json
import hashlib

cfgarr = None
tasks = []
#sqlconn = sql.connect('db/tasks.db')

def main():
    global cfgarr
    cfgarr = cfgp.ConfigParser()
    cfgarr.read('taskqueue.cfg')
    print([i for i in cfgarr['tasks']])
    print([i for i in cfgarr['taskexamples']])
    app = web.Application([
        (r'%s/' % cfgarr['core']['prefix'], IndexHandler),
        (r'%s/static/(.*)' % cfgarr['core']['prefix'], web.StaticFileHandler, {'path':
            cfgarr['core']['staticpath']}),
        (r'%s/addtask' % cfgarr['core']['prefix'], AddHandler),
        (r'%s/tasks' % cfgarr['core']['prefix'], TaskHandler),
        (r'/ws', WSHandler)
        ], debug=True)
    app.listen(cfgarr['core']['port'])
    ioloop.IOLoop.instance().start()


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("templates/index.html", conf=cfgarr, nts=len(tasks))


class AddHandler(web.RequestHandler):
    def get(self):
        self.render("templates/addtask.html", conf=cfgarr, nts=len(tasks),
                cf=utils.casefix)


class TaskHandler(web.RequestHandler):
    def get(self):
        self.render("templates/tasks.html", conf=cfgarr, nts=len(tasks),
                tasks=tasks, cf=utils.casefix)


class WSHandler(websocket.WebSocketHandler):
    global tasks
    lastsent = None
    def open(self):
        print('Websocket opened.')
        #self.ping(bytes())

    def on_message(self, message):
        global tasks
        msg = message.split(' ')
        print(msg)
        if msg[0] == 'delete':
            toremove = int(msg[1])
            hl = hashlib.new('md5')
            hl.update(cfgarr['core']['adminpass'].encode('utf-8'))
            if toremove < len(tasks) and msg[2] == hl.hexdigest():
                del(tasks[toremove])
            self.ping(bytes())
        elif msg[0] == 'update':
            self.ping(bytes())
        elif msg[0] == 'addtask':
            print('adding song')
            ratask = ''
            for i in msg[1:]:
                ratask += i + ' '
            ratask = ratask[:len(ratask) - 1]
            ntask = ratask.split('@___@')
            tasks.append(ntask[:len(ntask) - 1])
        #print('Message received: %s' %(message))

    def on_pong(self, data):
        self.write_message(json.dumps(tasks))
        print('pong received')

    def on_close(self):
        print('Websocket closed.')

if __name__ == '__main__':
    main()
