from flask import render_template, flash, redirect, url_for, request , json 
import MySQLdb
from configparser import ConfigParser
from app import app, db
from app.forms import LoginForm, RegistrationForm, ProjectForm, SprintForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Project, Team#, team_user_table, team_project_table
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    pids = db.engine.execute("select project.project_id from project join team_project_table on"
                             " (project.project_id = team_project_table.project_id) join team on"
                             " (team_project_table.team_id = team.team_id) join team_user_table on"
                             " (team.team_id = team_user_table.team_id) where team_user_table.user_id = " + current_user.get_id())

    project_ids = []
    for pid in pids:
        project_ids.append(pid[0])
    return render_template('index.html', title='Home', project_ids=project_ids, getProjName=getProjName)


def getProjName(project_id :int):
    projName = db.engine.execute("select project.ProjName from project where project.project_id = "+project_id)

    pname = []
    for name in projName:
        pname.append(name[0])
    return str(pname[0])


@app.route('/logintest', methods=['GET', 'POST'])
def logintest():
    if current_user.is_authenticated:
        return redirect(url_for('index'))# try redirect to '/user/'+str(USer.query.get(iduser))'
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')# try redirect to '/user/'+str(USer.query.get(iduser))'
        return redirect(next_page)
    return render_template('testlogin.html',  title='Sign In', form=form)
	

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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/project/<project_id>')
@login_required
def project_endpoint(project_id):
    sprints_num = db.engine.execute("select Sprint_num from sprint join project_sprint_table on"
                                    " (sprint.sprint_id = project_sprint_table.sprint_id) join project on"
                                    " (project_sprint_table.project_id = project.project_id)"
                                    "where project.ProjName = '" + ProjName + "'")
    sprints_num2 = db.engine.execute("select Sprint_num from sprint join project_sprint_table on"
                                     " (sprint.sprint_id = project_sprint_table.sprint_id) join project on"
                                     " (project_sprint_table.project_id = project.project_id)"
                                     "where project.ProjName = '" + ProjName + "'")
    big = db.engine.execute("select SUM(Difficulty) from user_stories join user_stories_sprint_table on"
                            " (user_stories.user_stories_id = user_stories_sprint_table.user_stories_id) join sprint on"
                            " (user_stories_sprint_table.sprint_id = sprint.sprint_id) join project_sprint_table on"
                            " (sprint.sprint_id = project_sprint_table.sprint_id) join project on"
                            " (project_sprint_table.project_id = project.project_id)"
                            "where project.ProjName = '" + ProjName + "'").scalar()
    completeDiff = []
    totalDiff = []
    sprints = []
    for num in sprints_num:
        sprints.append(num[0])

    total = 0
    for num in sprints:
        little = db.engine.execute("select SUM(Difficulty) from user_stories join user_stories_sprint_table on"
                                   " (user_stories.user_stories_id = user_stories_sprint_table.user_stories_id) join sprint on"
                                   " (user_stories_sprint_table.sprint_id = sprint.sprint_id) join project_sprint_table on"
                                   " (sprint.sprint_id = project_sprint_table.sprint_id) join project on"
                                   " (project_sprint_table.project_id = project.project_id)"
                                   "where project.ProjName = '" + ProjName + "' and sprint.sprint_num = '" + str(
            num) + "'").scalar()
        total = total + int(little)
        completeDiff.append(total)
    for num in sprints_num2:
        totalDiff.append(int(big))
    ProjName = str(getProjName(project_id))
    return render_template('project.html', ProjName=ProjName, sprints=sprints, totalDiff=totalDiff, completeDiff=completeDiff, project_id=project_id)


@app.route('/CreateProject', methods=['GET', 'POST'])
@login_required
def CreateProject():
    teams = db.engine.execute('select team_name from team join team_user_table on (team.idteam = team_user_table.idteam) where team_user_table.iduser = '+current_user.get_id())
    team_names = []
    for name in teams:
        team_names.append(name[0])
        

    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(ProjName=form.ProjName.data, total_diff = 0)
        team = Team(team_name=form.team_name.data)
        ''' TEST VALUES '''
        '''
        iduser = current_user.get_id()
        idteamqry = db.engine.execute("select idteam from team where team.team_name = '"+ form.team_name.data+ "'")
        #team_user_tbl = team_user_table(iduser = current_user.get_id(), idteam = db.engine.execute("select idteam from team where team.team_name = '"+ form.team_name.data+"'"))
        #team_project_tbl = team_project_table(idteam = db.engine.execute("select idteam from team where team.team_name = '"+ form.team_name.data, idProject = db.engine.execute("select idProject from project where project.ProjName = '"+ form.ProjName.data+"'")+"'"))
        team_user_tbl = team_user_table(iduser = current_user.get_id(), idteam = idteamqry)

        idteam = db.engine.execute("select idteam from team where team.team_name = '"+ form.team_name.data+ "'")
        idprojectqry = db.engine.execute("select idProject from project where project.ProjName = '"+ form.ProjName.data+"'") 
        team_project_tbl = team_project_table(idteam= idteamqry, idProject = idprojectqry)
        '''
        db.session.add(project)
        db.session.add(team)
        team.projteams.append(project)
        team.userteams.append(current_user)
        #db.session.add(team_user_tbl)
        #db.session.add(team_project_tbl)
        db.session.commit()
        flash('Congratulations, you made a project!')
       # return render_template('index.html', title='Home', project=project)
        return redirect(url_for('index'))
    return render_template('CreateProject.html', title='Create Project', form=form, team_names=team_names)


@app.route('/createsprint')  # not finished. Im not sure what to do here. DO we need a Sprint Model?
@login_required
def create_sprint_endpoint():
    form = SprintForm()
    return render_template('createSprint.html', form=form)


@app.route('/deletecard')  # Pop up with warning and confirmation
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

    return render_template('team.html', member_ids=member_ids, getUsername=getUsername, getEmail=getEmail)


def getUsername(user_id):
    username = db.engine.execute("select username from user where user.user_id = "+user_id)

    name = []
    for user in username:
        name.append(user[0])

    return name[0]


def getEmail(user_id):
    email = db.engine.execute("select email from user where user.user_id = "+user_id)

    user_email = []
    for e in email:
        user_email.append(e[0])

    return user_email[0]


@app.route('/sprintmanage/<project_id>')
@login_required
def sprint_manage_endpoint(project_id):

    sprints = db.engine.execute("select sprint_id from project_sprint_table where project_sprint_table.project_id = "+project_id)
    # may have to use an order by start date to get them in the proper order

    sprintids = []
    for sprint in sprints:
        sprintids.append(sprint[0])

    pb = db.engine.execute("select user_stories_id from user_stories_sprint_table where user_stories_sprint_table.sprint_id in "
                           "(select sprint_id from project_sprint_table where project_sprint_table.project_id = "+project_id+")")

    prodBackIds = []
    for prodback in pb:
        prodBackIds.append(prodback[0])

    return render_template('sprintManagement.html', getSprintNum=getSprintNum, sprintids=sprintids, prodBackIds=prodBackIds, myfunction=getTitle, getDifficulty=getDifficulty, project_id=project_id)


def getSprintNum(sprint_id):
    sprint_num = db.engine.execute("select sprint_num from sprint where sprint_id = "+sprint_id)

    sprint = []
    for s in sprint_num:
        sprint.append(s[0])

    return sprint[0]


@app.route('/sprint/<idsprint>/<project_id>')
@login_required
def sprint_endpoint(idsprint, project_id):

    todo_us = db.engine.execute("select user_stories.user_stories_id from user_stories join user_stories_sprint_table on "
                                "(user_stories.user_stories_id = user_stories_sprint_table.user_stories_id) "
                                "where user_stories_sprint_table.sprint_id = "+idsprint+" and user_stories.status = 'To Do'")

    todo = []
    for user_story in todo_us:
        todo.append(user_story[0])

    inprogress_us = db.engine.execute("select user_stories.user_stories_id from user_stories join user_stories_sprint_table on (user_stories.user_stories_id = user_stories_sprint_table.user_stories_id) "
                                      "where user_stories_sprint_table.sprint_id = "+idsprint+" and user_stories.status = 'In Progress'")

    inprogress = []
    for ip_us in inprogress_us:
        inprogress.append(ip_us[0])

    done_us = db.engine.execute("select user_stories.user_stories_id from user_stories join user_stories_sprint_table on (user_stories.user_stories_id = user_stories_sprint_table.user_stories_id) "
                                "where user_stories_sprint_table.sprint_id = "+idsprint+" and user_stories.status = 'Done'")

    done = []
    for dn_us in done_us:
        done.append(dn_us[0])

    pb = db.engine.execute("select user_stories_id from user_stories_sprint_table where user_stories_sprint_table.sprint_id in "
                           "(select sprint_id from project_sprint_table where project_sprint_table.project_id = " + project_id + ")")

    prodBackIds = []
    for prodback in pb:
        prodBackIds.append(prodback[0])

    return render_template('Sprint.html', project_id=project_id, todo=todo, inprogress=inprogress, done=done, prodBackIds=prodBackIds, getTitle=getTitle, getDifficulty=getDifficulty)


def getCurrentSprint(project_id):
    curr_sprint = db.engine.execute("select sprint_id from sprint join ")


def getTitle(id:int):
    userstorytitle = db.engine.execute("select title from user_stories where user_stories.user_stories_id = "+id)

    title = []
    for t in userstorytitle:
        title.append(t[0])
    return str(title[0])


def getDifficulty(id:int):
    diff = db.engine.execute("select difficulty from user_stories where user_stories.user_stories_id = " + id)

    difficulty = []
    for d in diff:
        difficulty.append(d[0])
    return str(difficulty[0])


def getDescription(id:int):
    descrip = db.engine.execute("select description from user_stories where user_stories.user_stories_id = "+id)

    description = []
    for desc in descrip:
        description.append(desc[0])
    return description[0]


def getAcceptanceCriteria(id:int):
    accept = db.engine.ececute("select acceptance_criteria from user_stories where user_stories.user_stories_id = "+id)

    acceptance = []
    for acc in accept:
        acceptance.append(accept[0])
    return acceptance[0]










