from flask import render_template, request, redirect, make_response
from flask import current_app
from flask_login import login_required, logout_user, login_user, current_user
from . import auth
from ..models import User
from .. import vcode

from .. import db
from ..models import AccessLog

from datetime import datetime
from urllib.parse import urlparse

def get_referrer_endpoint(url):
    if url is not None:
        u = urlparse(url)
        for x in current_app.url_map.iter_rules():
            if x.match(x.subdomain+'|'+u.path) is not None:
                return x.endpoint

def get_opt_info():
    view_doc = current_app.view_functions[request.endpoint].__doc__
    view_path = request.path
    view_endpoint = request.endpoint

    s = [
        current_user.username, 
        view_doc, 
        view_path, 
        view_endpoint, 
        str(request.view_args), 
        request.referrer, 
        get_referrer_endpoint(request.referrer), 
        request.remote_addr
    ]

    return s

def write_access_log(s):
    x = AccessLog(username=s[0], desc=s[1], path=s[2], endpoint=s[3],
                  args=s[4], referrer=s[5], rfendpoint=s[6], addr=s[7])
    db.session.add(x)
    db.session.commit()

@auth.before_app_request
def before_request():
    if request.path == '/favicon.ico':
        return
        
    if current_user.is_authenticated and request.endpoint != 'static':
        s = get_opt_info()
        write_access_log(s)    

    return
    
@auth.route('/', methods=['GET', 'POST'])
def login():
    '''登录'''

    if request.method == 'GET':
        return render_template('auth/login.html')

    if request.method == 'POST':
        username = request.form.get('fname')
        password = request.form.get('fpwd')
        vcode = request.form.get('fcode')

        u = User.query.filter_by(username=username).first()
        if u == None:
            return render_template('auth/login.html')
        
        v = request.cookies.get('auth_code')

        if u.verify_password(password) and v == vcode:
            login_user(u)
            s = get_opt_info()
            write_access_log(s)
            return redirect('/main/show_rpt_sum_apart/20191127')
        else:
            return render_template('auth/login.html')

@auth.route('/makeimage')
def make_image():
    """生成验证码"""

    s = vcode.gen_rand_str()
    c = vcode.make_image(current_app.config['IMAGE_FONT'], s)
    rsp = make_response(c.getvalue())
    rsp.mimetype = "image/jpeg"

    rsp.set_cookie('auth_code', s)

    return rsp

@auth.route('/logout')
@login_required
def logout():
    '''退出'''

    logout_user()
    return redirect('/')
