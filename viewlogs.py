from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    f = open("short_log.txt", "r")
    log_contents = f.read()
    f.close()
    return log_contents

if __name__ == '__main__':
    app.run() 
