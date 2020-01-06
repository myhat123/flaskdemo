import vcode

from flask import Flask, Response
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hi')
def hi():
    x = vcode.make_image('/home/hzg/etc/wqy-microhei.ttc', 'abcd')
    return Response(x.getvalue(), mimetype='image/jpeg')
