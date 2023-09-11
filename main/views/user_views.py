from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from main import db
from main.forms import UserCreateForm, UserLoginForm
from main.models import User

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/mypage')
def mypage():
    user = User.query.filter_by(email=session['email']).first()
    global freeNum
    global payNum
    return render_template('user/mypage.html',
        freeNum=user.freeNum, payNum=user.payNum)


@bp.route('/admin')
def admin():
    return 0


@bp.route('/signup', methods=('GET','POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            user = User(email=form.email.data,
                        password=generate_password_hash(form.password1.data), 
                        freeNum=3, payNum=0)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('function.home'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('user/signup.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['email'] = user.email
            return redirect(url_for('function.home'))
        flash(error)
    return render_template('user/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    email = session.get('email')
    if email is None:
        g.user = None
    else:
        g.user = User.query.get(email)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('function.home'))

