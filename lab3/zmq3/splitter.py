import pickle
import time
import zmq
import constPipe

src = constPipe.SRC
prt = constPipe.SPLITTER_PORT

with open("input2.txt") as f:
    t_raw = f.read()

me = "splitter"

t_cleaned_up = ''.join(t_raw.splitlines()).replace(',', '')

t_sentence_splitted = t_cleaned_up.split('.')

context = zmq.Context()
push_socket = context.socket(zmq.PUSH)  # create a push socket


address = "tcp://" + src + ":" + prt  # how and where to connect
push_socket.bind(address)  # bind socket to address

time.sleep(0.5) # gives enough time for mappers to react and connect recv()
for sentence in t_sentence_splitted:
    # time.sleep(0.5) # to see the splitter and mappers at work 
    push_socket.send(pickle.dumps((me, sentence)))
    print("pushed:", sentence)