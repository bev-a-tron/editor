import flask
import json
import subprocess
import tempfile
import io

app = flask.Flask(__name__)

import sys
from subprocess import Popen, PIPE
from threading  import Thread

def tee(infile, *files):
    """Print `infile` to `files` in a separate thread."""
    def fanout(infile, *files):
        for line in iter(infile.readline, ''):
            for f in files:
                #import pdb; pdb.set_trace()  # XXX BREAKPOINT
                #f.write(line.decode())
        infile.close()
    t = Thread(target=fanout, args=(infile,)+files)
    t.daemon = True
    t.start()
    return t

def teed_call(cmd_args, **kwargs):
    stdout, stderr = [kwargs.pop(s, None) for s in ('stdout', 'stderr')]
    p = Popen(cmd_args,
              stdout=PIPE if stdout is not None else None,
              stderr=PIPE if stderr is not None else None,
              **kwargs)
    threads = []
    if stdout is not None: threads.append(tee(p.stdout, stdout, sys.stdout))
    if stderr is not None: threads.append(tee(p.stderr, stderr, sys.stderr))
    for t in threads: t.join() # wait for IO completion
    return p.wait()

@app.route('/execute', methods=['POST'])
def execute():
    data = json.loads(flask.request.data)
    code = data['code']

    code = 'print("foo")'
    tf = tempfile.NamedTemporaryFile()
    tf.file.write(bytes(code, 'utf-8'))
    tf.flush()

    fout, ferr = io.StringIO(), io.StringIO()
    exitcode = teed_call(["python", tf.name], stdout=fout, stderr=ferr)
    stdout = fout.getvalue()
    stderr = ferr.getvalue()

    return flask.jsonify({'out': stdout, 'err': stderr})

@app.route('/')
def base():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=True)
