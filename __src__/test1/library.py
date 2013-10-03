import tornado.gen
 
class Library():
 
    @tornado.gen.engine
    def ask(self, question, callback=None):
        
        # do a computation that doesn't block for a long time.
        result = "Why would you want to know about '{0}'".format(question)
        error = None
        callback(result, error)
 
    @tornado.gen.engine
    def check_failure(self, callback=None):
        error = "This is the error"
        callback(None, error)
