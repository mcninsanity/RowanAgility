from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import synonym

team_project_table = db.Table('team_project_table',
                db.Column('project_id', db.Integer, db.ForeignKey('project.project_id')),
                db.Column('team_id', db.Integer, db.ForeignKey('team.team_id'))
) 

team_user_table = db.Table('team_user_table',
                db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
                db.Column('team_id', db.Integer, db.ForeignKey('team.team_id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password_hash = db.Column(db.String(120))
    id = synonym('user_id')
   #user_team = relationship('Team', secondary = 'team_user_table')

    teams = db.relationship('Team', secondary=team_user_table, backref=db.backref('userteams', lazy = 'dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Project(db.Model):
    __tablename__ = 'project'
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProjName = db.Column(db.String(45))
    total_diff = db.Column(db.Integer)
    id = synonym('project_id')
   #proj_team = relationship('Team', secondary = 'team_project_table')
    teams = db.relationship('Team', secondary=team_project_table, backref=db.backref('projteams', lazy = 'dynamic'))

class Team(db.Model):
    __tablename__ = 'team'
    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(45))
    id = synonym('team_id')
    #team_proj = relationship('Project', secondary = 'team_project_table')
    
    #team_user = relationship('User', secondary = 'team_user_table' )


'''
class team_user_table(db.Model):
    idteam_user_table = db.Column(db.Integer, primary_key=True, autoincrement=True)
    iduser = db.Column(db.Integer)#, ForeignKey('user.idUser'))
    idteam = db.Column(db.Integer)#, ForeignKey('team.idteam'))
    id = synonym('idteam_user_table')
    #user = relationship(user, backref=backref("user_assoc"))
    #team = relationship(team, backref=backref("team_assoc"))

class team_project_table(db.Model):
    idteam_project_table = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idProject = db.Column(db.Integer)#, ForeignKey('project.idProject'))
    idteam = db.Column(db.Integer)#, ForeignKey('team.idteam'))
    id = synonym('idteam_project_table')
    #project = relationship(project, backref=backref("project_assoc"))
   # team = relationship(team, backref=backref("team_assoc"))    
#Uncomment top when needed
'''
'''
class Project(db.Model):
    idProject = db.Column(db.Integer, primary_key=True, autoincrement=True)
    projname = db.Column(db.String(45))
    totaldiff = db.Column(db.Integer)
    team_project = relationship("Project", primaryjoin="and_(Project.idProject==Team.idteam, Team.team_names=='name')")
    id = synonym('idProject')
    
    def __repr__(self):
         return '<Project {}>'.format(self.projname)

class Team(db.Model):
    idteam = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(45))
    id = synonym('idteam')

    def __repr__(self):
        return '<Team {}>'.format(self.team_name)
'''
    
