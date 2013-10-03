import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
import tornado.options
 
tornado.options.define("port", default=8000, help="Run on the given port", type=int)
 
import library
mylibrary = library.Library()
 
class WhateverHandler(tornado.web.RequestHandler):
 
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        print("get")
        future = tornado.gen.Task(mylibrary.ask, question="What's this?")
        response = yield future
        (result, error) = response.args
        if error:
            raise tornado.web.HTTPError(500, error)
        else:
            self.set_header("Content-type", "text/html")
 
            self.write("<p>result:</p>")
            self.write("<pre>{0}</pre>".format(result))
            self.write("<p>error:</p>")
            self.write("<pre>{0}</pre>".format(error))
            self.finish()
 
tornado.options.parse_command_line()
app = tornado.web.Application(
    handlers = [
        (r'/', WhateverHandler),
    ],
)
 
http_server = tornado.httpserver.HTTPServer(app)
http_server.listen(tornado.options.options.port)
ioloop = tornado.ioloop.IOLoop.instance()
 
ioloop.start()
