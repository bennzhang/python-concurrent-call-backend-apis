import logging

from flask import Flask, request, jsonify
import requests
import os
import datetime
import time
import json
import sys
from multiprocessing import Pool
import itertools
from functools import partial

"""Use Cases 
   We have a backend service $BACKEND_URL that does the real calculation on one input json string. 
In reality, we have an arry of such json strings, all calculations are independent to each other. 
we want to calculate all in fast way. 
   Then we build this web service accepting an array of json strings and calls BACKEND_URL service in parallel. 
"""

app = Flask(__name__)

BACKEND_URL='your-url-link'

@app.route('/heath')
def hello():
    """Return a friendly HTTP health check."""
    return 'I am running!!!'

@app.route('/api/matrix', methods=['POST'])
def test_api():
    """use case is: we have a list of json string input,
    each individual json will call backend webserice
    :post body is an array of json strings
    :return: $BACKEND_URL webservice returns
    :rtype: an array of json strings of  $BACKEND_URL returnss
    """
    content = request.json

    size=len(content)
    print size
    for i in range(size):
        content[i].update({'index':i})

    start_time = int(round(time.time() * 1000))
    
    # spread matrix to backend rest api call
    pool = Pool(processes=30)
    ret=pool.map(cal_one_string, content, chunksize=4)
    pool.close()

    # sort by array index
    ret.sort(lambda x,y : cmp(x[0], y[0]))
    total_time = int(round(time.time() * 1000)) - start_time

    # construct result array
    result = []
    for i in range(size):
        result.append(ret[i][1])

    print total_time
    return json.dumps(result)

def cal_one_string(json_str):
   index=json_str['index']
   """default_json
   """
   default_json = {"cal_time": 10000, "value1": 0.0, "value2": 0.0, "value3": 1.0}
   
   try:
       # set timeout to 10 seconds
       r=requests.post(BACKEND_URL,json=json_str, timeout=20)
   except requests.exceptions.Timeout:
       print "Timeout occurred"
       return index,default_json
   except ValueError:
       print "ValueError"
       return index,default_json 

   try:
       r.json()
   except ValueError:
       print "ValueError"
       print r.content
       return index,default_json
       
   return index,r.json()
	
@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=8080, debug=True)
    app.run(threaded=True,debug=True)
## [END app]

