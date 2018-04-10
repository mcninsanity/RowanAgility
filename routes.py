from flask import render_template, flash, redirect, url_for, request , json 
import MySQLdb
from configparser import ConfigParser
from app import app, db
from app.forms import LoginForm, RegistrationForm, ProjectForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Project, Team#, team_user_table, team_project_table
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    projects = db.engine.execute("select ProjName from project join team_project_table on"
                             " (project.idProject = team_project_table.idProject) join team on"
                             " (team_project_table.idteam = team.idteam) join team_user_table on"
                             " (team.idteam = team_user_table.idteam) where team_user_table.iduser = " + current_user.get_id())

    names = []
    for name in projects:
        names.append(name[0])
    return render_template('index.html', title='Home', names=names)


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

@app.route('/project/<ProjName>')
@login_required
def project_endpoint(ProjName):
    sprints = [1, 2, 3, 4]
    totalDiff = [50, 65, 80, 70]
    completeDiff = [0, 20, 33, 55]
    return render_template('project.html', ProjName=ProjName, sprints=sprints, totalDiff=totalDiff, completeDiff=completeDiff)


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

@app.route('/sprintmanage')
@login_required
def sprint_manage_endpoint(idproject):

    sprints = db.engine.execute("select idsprint from sprint_project_table where sprint_project_table.idproject = "+idproject)
    # may have to use an order by start date to get them in the proper order

    sprint_ids = []
    for sprint in sprints:
        sprint_ids.append(sprint[0])

    pb = db.engine.execute("select iduser_stories from user_stories_sprint_table where user_stories_sprint_table.idsprint in "
                           "(select idsprint from sprint_project_table where sprint_project_table.idproject = "+idproject+")")

    return render_template('sprintmanage.html', sprint_ids=sprint_ids)

@app.route('/sprint')
@login.required
def sprint_endpoint(idsprint):

    us = db.engine.execute("select iduser_stories from user_stories_sprint_table where user_stories_sprint_table.idsprint = "+idsprint)
    # plan is to have a function that gets called from the html file which will use the user story ids to populate a 'card'
    # object with the proper info to be displayed in a list
    user_story_ids = []

    for user_story in us:
        user_story_ids.append(user_story[0])

    return render_template('sprint.html', user_story_ids=user_story_ids)

'''
def createCard(iduser_stories):
     descrip = db.engine.execute("select Description from user_stories where user_stories.iduser_stories = "+iduser_stories)
     diff = db.engine.execute("select Difficulty from user_stories where user_stories.iduser_stories = "+iduser_stories)
     accept = db.engine.execute("select Acceptance_criteria from user_stories where user_stories.iduser_stories = "+iduser_stories)
     status = db.engine.execute("select status from user_stories where user_stories.iduser_stories = "+iduser_stories)
     
'''





