import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import time
import datetime
import os, sys
from SenseScript import *

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
    
    def post (self):
        WebCommand = self.get_argument ('command', '')
        WebValue = self.get_argument ('value', '')
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        
        if WebCommand == 'update':

            update_response = {}
            update_response['TempValue'] = str(GetValues("Temp")) + " " + chr(176) + "C"
            update_response['HumidityValue'] = str(GetValues("Humidity"))
            update_response['PressureValue'] = str(GetValues("Pressure"))
            self.write(json.dumps(update_response))
            return
        else:
            print('Command not recognised')


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler)],
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"))

    
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)
    print ("Listening on port:", options.port)
    main_loop = tornado.ioloop.IOLoop.instance()
    # Schedule event (5 seconds from now)
    #main_loop.call_later(5, DisplayValues)
    # Start main loop
    main_loop.start()
