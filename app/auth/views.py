from flask import render_template, request, redirect
from flask_login import login_required, logout_user, login_user
from . import auth
from ..models import User

@auth.route('/login', methods=['GET', 'POST'])
def login():
    #如果是get
    if request.method == 'GET':
        return render_template('auth/login.html')

    #如果是post,获取表单信息进行验证登录
    if request.method == 'POST':
        username = request.form.get('fname')
        password = request.form.get('fpwd')

        u = User.query.filter_by(username=username).first()
        if u == None:
            return render_template('auth/login.html')
        
        if u.verify_password(password):
            login_user(u)
            return redirect('/main/show_rpt_sum_apart/20191127')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/auth/login')