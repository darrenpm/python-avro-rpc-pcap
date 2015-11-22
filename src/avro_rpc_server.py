from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import avro.ipc as ipc
import avro.protocol as protocol
import avro.schema as schema

PROTOCOL = protocol.parse(open("../mail.avpr").read())
HOST = ('localhost', 5000)

class MailResponder(ipc.Responder):
    def __init__(self):
        ipc.Responder.__init__(self, PROTOCOL)

    def invoke(self, msg, req):
        if msg.name == 'send':
            message = req['message']
            return ("Sent message to " + message['to']
                    + " from " + message['from']
                    + " with body " + message['body'])
        else:
            raise schema.AvroException("unexpected message:", msg.getname())

class MailHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.responder = MailResponder()
        call_request_reader = ipc.FramedReader(self.rfile)
        call_request = call_request_reader.read_framed_message()
        resp_body = self.responder.respond(call_request)
        self.send_response(200)
        self.send_header('Content-Type', 'avro/binary')
        self.end_headers()
        resp_writer = ipc.FramedWriter(self.wfile)
        resp_writer.write_framed_message(resp_body)



if __name__ == '__main__':
    server = HTTPServer(HOST, MailHandler)
    server.allow_reuse_address = True
    server.serve_forever()