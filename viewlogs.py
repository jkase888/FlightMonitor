from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
def view_logs():
    f = open("short_log.txt", "r")
    log_contents = f.read()
    f.close()
    log_contents = log_contents.replace('\n', '<br>')
    return log_contents

@app.route('/long')
def view_raw_logs():
    f = open("raw_log.txt", "r")
    log_contents = f.read()
    f.close()
    log_contents = log_contents.replace('\n', '<br>')
    return log_contents

if __name__ == '__main__':
    app.run()
