import unittest
import library
import tornado.gen
 
class TestLibrary(unittest.TestCase):
 
     def setUp(self):
          self.my_library = library.Library()
 
     def tearDown(self):
          pass
 
     @tornado.gen.engine
     def test_ask(self):
          question = "What's up?"
          future = tornado.gen.Task(self.my_library.ask, question=question)
          response = yield future
          (result, error) = response.args
          if error:
               self.fail("Got an error:  {0}".format(error))
          else:
               self.assertEqual(result, "Why would you want to know about '{0}'".format(question))
 
     @tornado.gen.engine
     def test_failure(self):
          future = tornado.gen.Task(self.my_library.check_failure)
          response = yield future
          (result, error) = response.args
          if error:
               pass
          else:
               self.fail("No error when expected one!")
