#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023 Lorenzo Carbonell <a.k.a. atareao>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pika

class SimpleProducer:
    def __init__(self, host, port, queue):
        self._host = host
        self._port = port
        self._queue = queue
        self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(host,
                                          socket_timeout=2))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=queue)

    def send(self, message):
        self._channel.basic_publish(exchange="",
                                    routing_key=self._queue,
                                    body=message)

    def __del__(self):
        try:
            self._connection.close(reply_code=200, reply_text="Normal shutdown")
        except Exception as exception:
            print(exception)


if __name__ == "__main__":
    sp = SimpleProducer("localhost", 5672, "mi-cola")
    sp.send('{"src": "origen", "dst": "destination"}')
    sp.send('{"src": "origen", "dst": "destination"}')
