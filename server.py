import flask
import subprocess
import json
import tempfile
import io

app = flask.Flask(__name__)

def execute_code(code):
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

    stdout = open('stdout', 'r')
    stderr = open('stderr', 'r')

    data = {'stdout': stdout.read(), 'stderr': stderr.read()}
    stdout.close()
    stderr.close()
    return data


@app.route('/execute', methods=['POST'])
def execute():
    # fixme: don't decode this
    data = json.loads(flask.request.data.decode())
    code = data['code']
    result = execute_code(code)
    return flask.jsonify(result)

@app.route('/')
def base():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=True)
