#!/usr/bin/env python3

import argparse
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from html.parser import HTMLParser
import json
from flask import Flask, render_template
from jinja2 import Template

class MyHTMLParser(HTMLParser):
    payload = list()
    def get_data(self):
        return self.payload

    def handle_data(self, data):
        self.payload.append(str(data))

class S(BaseHTTPRequestHandler):
    def _set_html_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _set_json_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def _html(self, message):
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8") 

    def get_stat(self):
        jinja2_template_string = open("stat.html", 'rb').read()
        template = Template(jinja2_template_string.decode('utf-8'))
        with open('tasks.json') as outfile:
            data = json.load(outfile)
            page = template.render(result_list=data["taskList"])
            return page.encode("utf8")

    def get_task(self):
        task = ""
        counter = 0
        data = {}
        with open('tasks.json', 'r') as readfile:
            data = json.load(readfile)
            for t in data["taskList"]:
                if t[1] == "Not completed":
                    task = t
                    break
                counter += 1

        if not task == "":
            content = f"<html><body><h1>Task</h1><h2>{task[0]}</h2><h3>{counter}</h3></body></html>"
            task[1] = "In progress"
            with open('tasks.json', 'w') as outfile:
                json.dump(data, outfile)
        else:
            content = f"<html><body><h1>No active tasks</h1></body></html>"
        return content.encode("utf8") 

    def do_GET(self):
        self._set_html_headers()
        req_path = str(self.path)
        payload = ""
        if req_path == "/gettask":
            payload = self.get_task()
        elif req_path == "/getstat":
            payload = self.get_stat()
        else:
            payload = self._html("hi!")

        self.wfile.write(payload)

    def do_HEAD(self):
        self._set_html_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length)
        payload = post_data.decode()
        j = json.loads(payload)
        id = j['Task id']
        res = j['Task result']
        time = j['Time']

        data = {}
        with open('tasks.json', 'r') as outfile:
            data = json.load(outfile)
            t = data["taskList"][id]
            t[1] = "Completed"
            t[2] = str(res)
            t[3] = str(time)

        with open('tasks.json', 'w') as outfile:
            json.dump(data, outfile)

        self._set_json_headers()
        foo = {'Result': "OK"}
        json_data = json.dumps(foo)
        self.wfile.write(json_data.encode("utf8"))


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


def rewriteCurrentTaskFile():
    with open('empty_tasks.json', 'r') as readfile:
        data = json.load(readfile)
        with open('tasks.json', 'w') as outfile:
            json.dump(data, outfile)

if __name__ == "__main__":
    rewriteCurrentTaskFile()
    run()
