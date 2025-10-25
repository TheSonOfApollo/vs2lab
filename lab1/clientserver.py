"""
Client and server using classes
"""

import logging
import socket
from database import phoneNumbers

import const_cs
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long

class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))
        self._logger.info("Server initialized correctly!")


    # def serve(self):
    #     greeting = "Hello this is the server talking"
    #     """ Serve echo """
    #     self.sock.listen(1)
    #     while self._serving:  # as long as _serving (checked after connections or socket timeouts)
    #         try:
    #             # pylint: disable=unused-variable
    #             (connection, address) = self.sock.accept()  # returns new socket and address of client
    #             self._logger.info("Connection succes!") #debbuging message
    #             connection.send(greeting.encode('ascii'))
    #             self._logger.info("Greeting sent succesfully") #debbuging message
    #             while True:  # forever
    #                 data = connection.recv(1024)  # receive data from client
    #                 if not data:
    #                     break  # stop if client stopped
    #                 connection.send(data + "*".encode('ascii'))  # return sent data plus an "*"
    #                 self._logger.info("Echo complete")
    #             connection.close()  # close the connection
    #         except socket.timeout:
    #             pass  # ignore timeouts
    #     self.sock.close()
    #     self._logger.info("Server down.")


    def handler(self): 
        self.sock.listen(1)
        while self._serving: 
            try:
                (connection, adress) = self.sock.accept()
                self._logger.info("Connection established")
                while True: 
                    data = connection.recv(1024)
                    if not data: 
                        break
                    decodedData = data.decode("ascii")
                    decodedData.replace("b", "", 1) # remove "b" leftover from en-/decoding
                    decodedData = decodedData.capitalize() # capitalize key so there are no key conflicts
                    self._logger.info("Decoding received message")
                    try: 
                        info = phoneNumbers[decodedData]
                    except:
                        info = "no entry found"
                        self._logger.info("Key not found!")
                    finally: 
                        self._logger.info("Encoding...")
                        connection.send((decodedData + " : " + info).encode("ascii")) 
                        self._logger.info("Sending info back!")
                connection.close()
            except socket.timeout:
                pass
        self.sock.close()
        self._logger.info("Connection closed")
                    


class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))


    # def call(self, msg_in="Hello, world"):
    #     #recGreeting = self.sock.recv('ascii')
    #     #print(recGreeting)
    #     """ Call server """
    #     self.sock.send(msg_in.encode('ascii'))  # send encoded string as data
    #     data = self.sock.recv(1024)  # receive the response
    #     msg_out = data.decode('ascii')
    #     print(msg_out)  # print the result
    #     #self.sock.close()  # close the connection
    #     return msg_out


    def close(self):
        """ Close socket """
        self.logger.info("Client down.")
        self.sock.close()

    def get(self, name = ""):
        if not str(name).isalpha():
            self.logger.info("Invalid request, parameter isn't alphanumeric")
            print("This is an invalid request --> '" + str(name) + "'")
            print("Please use only letters from the alphabet!")
        else: 
            self.sock.send(name.encode("ascii")) #send reqested name
            self.logger.info("Sent name: " + name) 
            self.logger.info(name.encode("ascii")) # debbuging message, delete later
            info = self.sock.recv(1024)
            self.logger.info("Information received, decoding...")
            info_out = info.decode("ascii")
            print(info_out)
            return(info_out) 

    def getAll(self): 
        command = "---GET_ALL---"
        info = ""
        self.sock.send(command.encode("ascii")) 
        self.logger.info("Requesting ALL contacts...")
        while info != "---FINISHED---": 
            info = self.sock.recv(1024)
            info_out = info.decode("ascii")
            print(info_out)
        self.logger.info("All contacts received succesflully")
        print("All contacts received succesflully")
        
         
    # def first(self):
    #     recGreeting = self.sock.recv(1024) #recv parameter = number of characters, here 1024 characters!
    #     decoded = recGreeting.decode('ascii')
    #     print(decoded)
    #     return(decoded)
