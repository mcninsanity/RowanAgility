from flask import render_template, flash, redirect, url_for, request, json
from app import app, db
from app.forms import LoginForm, RegistrationForm, ProjectForm, SprintForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Project, Team, Sprint
from werkzeug.urls import url_parse
import datetime


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    proj_ids = db.engine.execute("select project.project_id from project join team_project_table on"
                             " (project.project_id = team_project_table.project_id) join team on"
                             " (team_project_table.team_id = team.team_id) join team_user_table on"
                             " (team.team_id = team_user_table.team_id) where team_user_table.user_id = " + current_user.get_id())

    project_ids = []
    for pid in proj_ids:
        project_ids.append(pid[0])
    return render_template('index.html', title='Home', project_ids=project_ids, get_proj_name=get_proj_name)


def get_proj_name(project_id:int):
    proj_name = db.engine.execute("select project.proj_name from project where project.project_id = "+project_id)

    pname = []
    for name in proj_name:
        pname.append(name[0])
    return str(pname[0])


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
    return render_template('login.html',  title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # only accept alphanumeric characters for username
        if form.username.data.isalnum() is True:

            user = User(username=form.username.data, email=form.email.data)

            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        else:
            flash('Please use alphanumeric characters for username.')
    return render_template('register.html', title='Register', form=form)


@app.route('/project/<project_id>')
@login_required
def project_endpoint(project_id):
    sprints = [1, 2, 3, 4]
    totalDiff = [50, 65, 80, 70]
    completeDiff = [0, 20, 33, 55]
    ProjName = str(get_proj_name(project_id))
    return render_template('project.html', title="Project page", ProjName=ProjName, sprints=sprints, totalDiff=totalDiff, completeDiff=completeDiff, project_id=project_id)


@app.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    teams = db.engine.execute('select team_name from team join team_user_table on (team.team_id = team_user_table.team_id) where team_user_table.user_id = '+current_user.get_id())
    team_names = []
    for name in teams:
        team_names.append(name[0])

    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(proj_name=form.proj_name.data, total_diff=0)
        team = Team(team_name=form.team_name.data)

        db.session.add(project)
        db.session.add(team)
        team.projteams.append(project)
        team.userteams.append(current_user)
        db.session.commit()
        flash('Congratulations, you made a project!')
        return redirect(url_for('index'))
    return render_template('CreateProjectNew.html', title='Create Project', form=form, team_names=team_names)


@app.route('/delete_project/<project_id>')
@login_required
def delete_project(project_id):
    if current_user.is_authenticated:
        project = Project.query.filter_by(project_id=project_id).first()

        if not project:
            flash('Project not found!')

        db.session.delete(project)
        db.session.commit()
        flash('Project successfully deleted!')
        return redirect(url_for('index'))


@app.route('/create_sprint')  # not finished. Im not sure what to do here. DO we need a Sprint Model?
@login_required
def create_sprint_endpoint():
    form = SprintForm()
    if form.validate_on_submit():
        sprint = Sprint(start_date=form.start_date, end_date=datetime.datetime.utcnow() + datetime.timedelta(days=14)) # add 2 weeks to same day its generated

        db.session.add(sprint)
        db.session.commit()
        flash('Sprint has been generated!')
        return redirect(url_for('login'))
    return render_template('createSprint.html', form=form)


@app.route('/delete_card')  # Pop up with warning and confirmation
def delete_card(user_stories_id):

    db.engine.ececute("delete * from user_stories where user_stories.user_stories_id = "+user_stories_id)
    db.engine.ececute("delete * from user_stories_sprint_table where user_stories_sprint_table.user_stories_id = " + user_stories_id)
    db.engine.ececute("delete * from user_user_stories_table where user_user_stories_table.user_stories_id = " + user_stories_id)
    db.engine.ececute("delete * from to_do where to_do.user_stories_id = " + user_stories_id)
    db.engine.ececute("delete * from works_on where works_on.user_stories_id = " + user_stories_id)
    db.engine.ececute("delete * from requirements where requirements.user_stories_id = " + user_stories_id)


@app.route('/team/<project_id>')
@login_required
def team_endpoint(project_id):
  
    members = db.engine.execute("select user.user_id from user join team_user_table on (user.user_id = team_user_table.user_id) "
                                "join team on (team_user_table.team_id = team.team_id) join team_project_table on (team.team_id = team_project_table.team_id) "
                                "join project on (team_project_table.project_id = project.project_id) where project.project_id = "+project_id)
  
    member_ids = []
    for id in members:
        member_ids.append(id[0])

    return render_template('team.html', title="Team", member_ids=member_ids, get_username=get_username, get_email=get_email)


def get_username(user_id):
    username = db.engine.execute("select username from user where user.user_id = "+user_id)

    name = []
    for user in username:
        name.append(user[0])

    return name[0]


def get_email(user_id):
    email = db.engine.execute("select email from user where user.user_id = "+user_id)

    user_email = []
    for e in email:
        user_email.append(e[0])

    return user_email[0]

# add this later? or make another endpoint to create a github link
#def addGithublink():


@app.route('/sprint_manage/<project_id>')
@login_required
def sprint_manage_endpoint(project_id):

    sprints = db.engine.execute("select sprint_id from project_sprint_table where project_sprint_table.project_id = "+project_id)
    # may have to use an order by start date to get them in the proper order

    sprint_ids = []
    for sprint in sprints:
        sprint_ids.append(sprint[0])

    pb = db.engine.execute("select user_stories_id from user_stories_sprint_table where user_stories_sprint_table.sprint_id in "
                           "(select sprint_id from project_sprint_table where project_sprint_table.project_id = "+project_id+")")

    prod_back_ids = []
    for prod_back in pb:
        prod_back_ids.append(prod_back[0])

    return render_template('sprintManagement.html', title="Sprint Management", get_sprint_num=get_sprint_num, sprint_ids=sprint_ids, prod_back_ids=prod_back_ids, myfunction=get_title, get_difficulty=get_difficulty, project_id=project_id)


def get_sprint_num(sprint_id):
    sprint_num = db.engine.execute("select sprint_num from sprint where sprint_id = "+sprint_id)

    sprint = []
    for s in sprint_num:
        sprint.append(s[0])

    return sprint[0]


@app.route('/sprint/<sprint_id>/<project_id>')
@login_required
def sprint_endpoint(sprint_id, project_id):

    todo_us = db.engine.execute("select user_stories.user_stories_id from user_stories join user_stories_sprint_table on "
                                "(user_stories.user_stories_id = user_stories_sprint_table.user_stories_id) "
                                "where user_stories_sprint_table.sprint_id = "+sprint_id+" and user_stories.status = 'To Do'")

    todo = []
    for user_story in todo_us:
        todo.append(user_story[0])

    inprogress_us = db.engine.execute("select user_stories.user_stories_id from user_stories join user_stories_sprint_table on (user_stories.user_stories_id = user_stories_sprint_table.user_stories_id) "
                                      "where user_stories_sprint_table.sprint_id = "+sprint_id+" and user_stories.status = 'In Progress'")

    in_progress = []
    for ip_us in inprogress_us:
        in_progress.append(ip_us[0])

    done_us = db.engine.execute("select user_stories.user_stories_id from user_stories join user_stories_sprint_table on (user_stories.user_stories_id = user_stories_sprint_table.user_stories_id) "
                                "where user_stories_sprint_table.sprint_id = "+sprint_id+" and user_stories.status = 'Done'")

    done = []
    for dn_us in done_us:
        done.append(dn_us[0])

    pb = db.engine.execute(
        "select user_stories_id from user_stories_sprint_table where user_stories_sprint_table.sprint_id in "
        "(select sprint_id from project_sprint_table where project_sprint_table.project_id = " + project_id + ")")

    prod_back_ids = []
    for prod_back in pb:
        prod_back_ids.append(prod_back[0])

    return render_template('Sprint.html', title="Sprint Page", project_id=project_id, todo=todo, in_progress=in_progress, done=done, prod_back_ids=prod_back_ids, get_title=get_title, get_difficulty=get_difficulty)


def get_current_sprint(project_id):
    curr_sprint = db.engine.execute("select sprint_id from sprint join ")


def get_title(id:int):
    user_story_title = db.engine.execute("select title from user_stories where user_stories.user_stories_id = "+id)

    title = []
    for t in user_story_title:
        title.append(t[0])
    return str(title[0])


def get_difficulty(id:int):
    diff = db.engine.execute("select difficulty from user_stories where user_stories.user_stories_id = " + id)

    difficulty = []
    for d in diff:
        difficulty.append(d[0])
    return str(difficulty[0])










