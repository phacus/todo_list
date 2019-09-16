from todo_list import app, db
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from todo_list.models import User, Task

import datetime

# views
@app.route('/', methods=['GET', 'POST'])
def index():
    # form input
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Please Login.')
            return redirect(url_for('index'))
        title = request.form.get('title')
        create_time = datetime.datetime.now()
        user_id = current_user.get_id()
        # check if valid
        if not title or len(title) > 20:
            flash('Invalid input.')
            return redirect(url_for('index'))
        task = Task(title=title, create_time=create_time, user_id=user_id)
        db.session.add(task)
        db.session.commit()
        flash('Task created.')
        return redirect(url_for('index'))

    tasks = Task.query.filter(Task.user_id == current_user.get_id())
    return render_template('index.html', tasks=tasks)


@app.route('/task/update/<int:task_id>', methods=['GET', 'POST'])
@login_required
def update(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        title = request.form['title']
        if not title or len(title) > 20:
            flash('Invalid input.')
            return redirect(url_for('update', task_id=task_id))
        task.title = title
        task.create_time = datetime.datetime.now()
        db.session.commit()
        flash('Task updated.')
        return redirect(url_for('index'))
    return render_template('update.html', task=task)


@app.route('/task/delete/<int:task_id>', methods=['POST'])
@login_required
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()

        if user is not None:
            if user.username == username and user.validate_password(password):
                login_user(user)
                flash('Login success.')
                return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('8888888888888888888888')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        check_pw = request.form['check_pw']

        if not username or not password or not check_pw:
            flash('Invalid input.')
            return redirect(url_for('register'))

        user = User.query.filter_by(username=username).first()
        if user is not None:
            flash('使用者名稱已存在')
            return redirect(url_for('register'))

        if password != check_pw:
            flash('密碼不一致')
            return redirect(url_for('register', username=username))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('註冊成功 請重新登入')
        return redirect(url_for('login', username=username))

    return render_template('register.html')


@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % name
