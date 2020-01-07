from flask import render_template, request, redirect, make_response
from flask import current_app
from flask_login import login_required, logout_user, login_user
from . import auth
from ..models import User
from .. import vcode

@auth.route('/login', methods=['GET', 'POST'])
def login():
    #如果是get
    if request.method == 'GET':
        return render_template('auth/login.html')

    #如果是post,获取表单信息进行验证登录
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
    logout_user()
    return redirect('/auth/login')