#!/usr/bin/env python3

import pickle, json

# load data from pickle file
#with open('repos_table.pickle', 'rb') as f:
#  mapping = pickle.load(f)

mapping = [
    [1,3,4,5,6,7,9,12],
    [1,3,4,5,6,7,9,12],
    [1,3,4,5,6,7,9,12],
    [1,3,4,5,6,7,9,12],
        ]

def dumppickle(file_name,mapping):
    with open(file_name, 'wb') as f:
        pickle.dump(mapping, f)

# mapping == [repo_name,repo_old_address,repo_web_address,repo_git_address,dry_run_status,git_push_status,lock_status,branches_number,repo_size]

# sorted by time mapping
def my_int(i):
    if i == 'ERROR':
        return 999999
    if i == '':
        return 99999
    return int(i.split('.')[0])

# flask
from flask import Flask, flash, redirect, render_template, request, session, abort, Response
 
app = Flask(__name__)
 
@app.route("/")
def index():
    return "Flask App!"


# Main table - displays all repositories with statuses
@app.route("/table/")
def show_table():
    return render_template('table.html',lst=mapping)

# Main table - displays all repositories with statuses
@app.route("/table2/")
def show_table2():
    return render_template('table2.html',lst=mapping)

# Main table - displays all repositories with statuses sorted
@app.route("/table3/")
def show_table3():
    return render_template('table2.html',lst=list(reversed(sorted(mapping,key = lambda mm: my_int(mm[4])))))

# GET requests for taking tasks: GET /getapi/?startswith=ab ; GET /getapi/?startswith=ab&param=4
# param 4 - dry-run status
# param 5 - git push --all status
@app.route('/getapi/', methods=['GET'])
def gettasks():
    param = request.args.get("param")
    starts = request.args.get("startswith")
    if not param:
        if starts:
            answer = [ m for m in mapping if (m[0].startswith(starts)) ]
        else:
            answer = [ m for m in mapping ]
    else:
        r=int(param)
        if starts:
            answer = [ m for m in mapping if (m[r] == '') and (m[0].startswith(starts)) ]
        else:
            answer = [ m for m in mapping if (m[r] == '') ]
    answer = { "results": answer }
    json_response=json.dumps(answer)
    response=Response(json_response,content_type='application/json; charset=utf-8')
    response.headers.add('content-length',len(json_response))
    response.status_code=200
    return response

# GET requests for iterating through tasks: GET /getlock/
# server gives task to client and locks it until client updates task status
@app.route('/getlock/', methods=['GET'])
def get_and_lock():
    answer = None
    for m in mapping:
        if (m[4] == '') and (m[6] == ''):
            answer = m
            m[6] = str(request.remote_addr)
            dumppickle('repos_table.pickle',mapping)
            break
    answer = { "results": answer }
    json_response=json.dumps(answer)
    response=Response(json_response,content_type='application/json; charset=utf-8')
    response.headers.add('content-length',len(json_response))
    response.status_code=200
    return response


# POST api: POST /updateapi/
@app.route('/updateapi/', methods = ['POST'])
def update_data():
    req_data = request.json
    print(req_data)
    repo_data = req_data["data"]
    for mp in mapping:
        if mp[0] == repo_data[0]:
            mp[4:] = repo_data[4:]
    dumppickle('repos_table.pickle',mapping)
    answer = { "results": repo_data }
    json_response=json.dumps(answer)
    response=Response(json_response,content_type='application/json; charset=utf-8')
    response.headers.add('content-length',len(json_response))
    response.status_code=200
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
