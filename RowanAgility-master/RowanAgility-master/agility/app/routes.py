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
    sprints = [1, 2, 3, 4]
    totalDiff = [50, 65, 80, 70]
    completeDiff = [0, 20, 33, 55]
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

@app.route('/createsprint')
@login_required
def create_sprint_endpoint():
    form = SprintForm()
    return render_template('createSprint.html', form=form)
#@app.route('/team/<ProjName>')
#@login_required
#def team_endpoint(ProjName):
  
 #   members = db.engine.execute("select username from user join team_user_table on (user.iduser = team_user_table.iduser) "
 #                               "join team on (team_user_table.idteam = team.idteam) join team_project_table on (team.idteam = team_project_table.idteam) "
  #                              "join project on (team_project_table.idproject = project.idproject) where project.ProjName = '{ProjName}'".format(ProjName=ProjName))
  
   # teamnames = []
    #for teamname in members:
     #   teamnames.append(teamname[0])
   
    #return render_template('team.html', teamnames=teamnames)

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

    return render_template('sprintManagement.html', sprintids=sprintids, prodBackIds=prodBackIds, myfunction=getTitle, getDifficulty=getDifficulty)

@app.route('/sprint/<idsprint>')
@login_required
def sprint_endpoint(idsprint):

    todo_us = db.engine.execute("select user_stories.user_stories_id from user_stories join user_stories_sprint_table on "
                                "(user_stories.user_stories_id = user_stories_sprint_table.user_stories_id) "
                                "where user_stories_sprint_table.sprint_id = "+idsprint+" and user_stories.status = 'To Do'")

    todo = []
    for user_story in todo_us:
        todo.append(us[0])

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

    return render_template('Sprint.html', todo=todo, inprogress=inprogress, done=done)


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










