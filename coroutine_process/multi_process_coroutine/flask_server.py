from flask import Flask
import time

app = Flask(__name__)
count_uid=0
@app.route('/')
def index():
    global count_uid
    time.sleep(3)
    count_uid=count_uid+1
    return 'Hello!'+str(count_uid)

if __name__ == '__main__':
    app.run(threaded=True)