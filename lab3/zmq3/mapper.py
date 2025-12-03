import pickle
import sys
import zmq

import constPipe

address_pull = "tcp://" + constPipe.SRC + ":" + constPipe.SPLITTER_PORT  # all mappers connect to the same source  

address_push_1 = "tcp://" + constPipe.SRC + ":" + constPipe.PORT2  # how and where to connect
address_push_2 = "tcp://" + constPipe.SRC + ":" + constPipe.PORT3  # how and where to connect

me = str(sys.argv[1])
context = zmq.Context()
pull_socket = context.socket(zmq.PULL)  # create a pull socket
pull_socket.connect(address_pull)  # connect to task source

push_socket_1 = context.socket(zmq.PUSH)  # create a push socket
push_socket_1.connect(address_push_1)  # bind socket to address

push_socket_2 = context.socket(zmq.PUSH)  # create a push socket
push_socket_2.connect(address_push_2)  # bind socket to address



print(f"{me} started")

while True:
    work = pickle.loads(pull_socket.recv())  # receive work from a source
    print("{} received workload '{}' from {}".format(me, work[1], work[0]))
    words = work[1].strip().split(' ')

    # Hash word
    # word mod reducer.count
    # send to reducer

    for word in words:
        if not word: 
            continue

        reducer_id = hash(word) % 2
        if reducer_id > 0:
            print(f"push {reducer_id}:", word)
            #push_socket_2.send(pickle.dumps((me, word)))
        else:
            print(f"push {reducer_id}:", word)
            #push_socket_1.send(pickle.dumps((me, word)))




    