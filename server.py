import flask
import json
import subprocess
import tempfile
import io

app = flask.Flask(__name__)

import sys
from subprocess import Popen, PIPE
from threading  import Thread


@app.route('/execute', methods=['POST'])
def execute():
    data = json.loads(flask.request.data)
    code = data['code']

    code = 'print("foo")'
    tf = tempfile.NamedTemporaryFile()
    tf.file.write(bytes(code, 'utf-8'))
    tf.flush()

    # fout, ferr = io.StringIO(), io.StringIO()

    stdout = open('stdout', 'w+')
    stderr = open('stderr', 'w+')
    exitcode = subprocess.call(["python", tf.name], stdout=stdout, stderr=stderr)
    #stdout = fout.getvalue()
    #stderr = ferr.getvalue()
    stdout.close()
    stderr.close()

    stdout = open('stdout', 'r').read()
    stderr = open('stderr', 'r').read()

    data = {'out': stdout, 'err': stderr}
    stdout.close()
    stderr.close()
    return flask.jsonify(data)

@app.route('/')
def base():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=True)
