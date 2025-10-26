"""
Simple client server unit test
"""
import textwrap
import logging
import threading
import unittest
import io
from contextlib import redirect_stdout

import clientserver
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class TestEchoService(unittest.TestCase):
    """The test"""
    _server = clientserver.Server()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.handler)  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = clientserver.Client()  # create new client for each test

    # def test_srv_get(self):  # each test_* function is a test
    #     """Test simple call"""
    #     msg = self.client.call("Hello VS2Lab")
    #     self.assertEqual(msg, 'Hello VS2Lab*')

    def test_simple_get(self): 
        msg = self.client.get("Alice")
        self.assertEqual(msg, "Alice : +49 671 6367577")

    def test_capslock_get(self): 
        msg = self.client.get("CARLOS")
        self.assertEqual(msg, "Carlos : +49 957 0269783")

    def test_number_get(self): 
        f = io.StringIO()
        with redirect_stdout(f): 
            msg = self.client.get(32)
        output = f.getvalue().strip()
        self.assertIn("This is an invalid request --> '32'", output)
        self.assertIn("Please use only letters from the alphabet!", output)
        self.assertIsNone(msg) # no response cuz invalid input
         
    def test_numberAsString_get(self): 
        f = io.StringIO()
        with redirect_stdout(f): 
            msg = self.client.get("9")
        output = f.getvalue().strip()
        self.assertIn("This is an invalid request --> '9'", output)
        self.assertIn("Please use only letters from the alphabet!", output)
        self.assertIsNone(msg) # no response cuz invalid input
   
    def test_mixInvalidInput_get(self): 
        f = io.StringIO()
        with redirect_stdout(f): 
            msg = self.client.get("22BoB22")
        output = f.getvalue().strip()
        self.assertIn("This is an invalid request --> '22BoB22'", output)
        self.assertIn("Please use only letters from the alphabet!", output)
        self.assertIsNone(msg) # no response cuz invalid input
   
    def test_numberInString_get(self): 
        f = io.StringIO()
        with redirect_stdout(f): 
            msg = self.client.get("R0bert")
        output = f.getvalue().strip()
        self.assertIn("This is an invalid request --> 'R0bert'", output)
        self.assertIn("Please use only letters from the alphabet!", output)
        self.assertIsNone(msg) # no response cuz invalid input
    
    def test_void_get(self):
        f = io.StringIO()
        with redirect_stdout(f): 
            msg = self.client.get()
        output = f.getvalue().strip()
        self.assertIn("This is an invalid request --> ''", output)
        self.assertIn("Please use only letters from the alphabet!", output)
        self.assertIsNone(msg) # no response cuz invalid input

    def test_empty_get(self):
        f = io.StringIO()
        with redirect_stdout(f): 
            msg = self.client.get("")
        output = f.getvalue().strip()
        self.assertIn("This is an invalid request --> ''", output)
        self.assertIn("Please use only letters from the alphabet!", output)
        self.assertIsNone(msg) # no response cuz invalid input

    def test_inexistentKey_get(self):
        msg = self.client.get("Cooper")
        self.assertEqual(msg, "Cooper : no entry found")

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate


if __name__ == '__main__':
    unittest.main()
