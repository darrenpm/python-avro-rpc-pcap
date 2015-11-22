import sys

import avro.ipc as ipc
import avro.protocol as protocol

PROTOCOL = protocol.parse(open("../mail.avpr").read())

server_addr = ('localhost', 5000)

class UsageError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise UsageError("Usage: <to> <from> <body>")

    # client code - attach to the server and send a message
    client = ipc.HTTPTransceiver(server_addr[0], server_addr[1])
    requestor = ipc.Requestor(PROTOCOL, client)
    
    # fill in the Message record and send it
    message = dict()
    message['to'] = sys.argv[1]
    message['from'] = sys.argv[2]
    message['body'] = sys.argv[3]

    params = dict()
    params['message'] = message
    print("Result: " + requestor.request('send', params))

    # cleanup
    client.close()