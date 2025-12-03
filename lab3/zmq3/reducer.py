import pickle
import sys
import zmq

import constPipe


me = str(sys.argv[1])

address_pull_1 = "tcp://" + constPipe.SRC + ":" + constPipe.PORT2   
address_pull_2 = "tcp://" + constPipe.SRC + ":" + constPipe.PORT3  

address = address_pull_1 if me == '1' else address_pull_2
context = zmq.Context()

pull_socket = context.socket(zmq.PULL)  # create a pull socket
pull_socket.bind(address)  # connect to task source

print(f"{me} started")

counter = 0
word_counts = {}

while True:
    work = pickle.loads(pull_socket.recv())
    sender, word = work

    print(f"Reducer {me} received word '{word}' from {sender}")

    # Update counters
    counter += 1
    word_counts[word] = word_counts.get(word, 0) + 1

    print(f"Total words so far: {counter}")