    from flask import render_template, flash, redirect, url_for, request
    from app import app, db
    from app.forms import LoginForm, RegistrationForm
    from flask_login import current_user, login_user, logout_user, login_required
    from app.models import User
    from werkzeug.urls import url_parse


    def homebutton_click():
        return redirect(url_for('user')


    def log_out_click():
        return redirect(url_for('logout'))


    def sprint_management_click():


    def current_sprint_click():


    def github_link_click():


    def team_page_click():



    @app.route('/')
    @app.route('/index')
    @login_required
    def index():
        posts = [
            {
                'author': {'username': 'John'},
                'body': 'Let\'s knock some PBI down this week.'
            },
            {
                'author': {'username': 'Susan'},
                'body': 'Good burn-up team!'
            }
        ]
        return render_template('index.html', title='Home', posts=posts)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        return render_template('login.html', title='Sign In', form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)

    @app.route('/project', methods=['GET', 'POST'])
    @login_required
    def project():

        sprints = [0, 1, 2, 3, 4]
        totalDiff = [50, 50, 65, 80, 70]
        completeDiff = [0, 10, 20, 33, 55]

        return render_template('project.html', sprints=sprints, totalDiff=totalDiff, completeDiff=completeDiff)

