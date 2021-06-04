#!/usr/bin/env python3
"""
Very simple HTTP server in python (Updated for Python 3.7)
Usage:
    ./dummy-web-server.py -h
    ./dummy-web-server.py -l localhost -p 8000
Send a GET request:
    curl http://localhost:8000
Send a HEAD request:
    curl -I http://localhost:8000
Send a POST request:
    curl -d "foo=bar&bin=baz" http://localhost:8000
This code is available for use under the MIT license.
----
Copyright 2021 Brad Montgomery
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.    
"""
import http.client
from html.parser import HTMLParser
import sympy
import json
import time

class MyHTMLParser(HTMLParser):
    payload = list()
    def get_data(self):
        return self.payload

    def handle_data(self, data):
        print("Encountered some data :", data)
        self.payload.append(str(data))

connection = http.client.HTTPConnection('localhost', 8000)
connection.request("GET", "/gettask")
response = connection.getresponse()
print("Status: {} and reason: {}".format(response.status, response.reason))
headers = response.getheaders()
print(headers)

data = response.read().decode()
parser = MyHTMLParser()
parser.feed(data)
payload = parser.get_data()
print(payload)

status = payload[0]

if status == "Task":
    task = payload[1].split(" ")
    id = int(payload[2])
    type = task[0]
    number = int(task[1])
    power = int(task[2])
    t1 = time.time()
    res = False
    if type == "IsPrime":
        res = sympy.isprime(number**power - 1)
    t2 = time.time()
    timeInMs = round(t2 - t1, 10)
    print(type + " " + str(res))
    print("Time: " + str(timeInMs))
    

    foo = {'Task id': id, 'Task result': res, 'Time': timeInMs }
    json_data = json.dumps(foo)

    headers = {'Content-type': 'application/json', 'Content-Length':len(json_data)}

    connection.request('POST', '/post', json_data, headers)

    response = connection.getresponse()
    respstat = response.read().decode()
    print(respstat)

connection.close()