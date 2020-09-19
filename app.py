import os
import subprocess

import requests
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/matching/<path:request>', methods=['GET', 'POST'])
def matching(request):
    r = request
    url = r
    print(url)
    link = url.split('.')
    try:
        r = requests.get(url, allow_redirects=True)
    except:
        return "Audio not downloadable"
    open('media/1' + "." + link[-1], 'wb').write(r.content)
    print("saved")
    subprocess.run(
        "python print_matching_test.py match --dbase fpdbase.pklz --min-count 1 {context}".format(
            context='1' + "." + link[-1]),
        shell=True)
    # try:
    with open('result.txt') as f:
        g = f.read()
        result = g.replace("audios\\", '')
        result = result.split('.')[0]
            # print(result)
        return result
    # except:
    #     return "Audio not found in database"


@app.route('/add_fingprint/<path:url>/<int:id>', methods=['Get', 'POST'])
def add_fingprint(url, id):
    print(url)
    print(id)
    link = url.split('.')
    r = requests.get(url, allow_redirects=True)
    open('media/' + str(id) + "." + link[-1], 'wb').write(r.content)
    print("saved")
    subprocess.run(
        "python audfprint.py add --dbase fpdbase.pklz {context}".format(context='media/' + str(id) + "." + link[-1]),
        shell=True)
    os.remove('media/' + str(id) + "." + link[-1])
    return 'Added in database'


if __name__ == '__main__':
    app.run()
