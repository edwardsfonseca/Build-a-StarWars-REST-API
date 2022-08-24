from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class People(db.Model):
    __tablename__:"people"
    uid = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50),unique=True,nullable=False)
    height=db.Column(db.Integer,unique=False,nullable=False)
    hair_color=db.Column(db.String(40),unique=False,nullable=False)
    gender=db.Column(db.String(40),unique=False,nullable=False)
    
    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "height":self.height,
            "hair_color":self.hair_color,
            "gender":self.gender
            # do not serialize the password, its a security breach
        }
class FavPeople(db.Model):
    __tablename__:"favpeople"
    id = db.Column(db.Integer, primary_key=True)
    user=db.Column(db.String(120),db.ForeignKey('user.email'))
    people=db.Column(db.Integer,db.ForeignKey('people.uid'))
    rel_1=db.relationship('User')
    rel_2=db.relationship('People')
    def __repr__(self):
        return '<FavPeople %r>' % self.id

    def serialize(self):
        return {
            "uid": self.uid,
            "user": self.user,
            "people":self.people
            # do not serialize the password, its a security breach
        }
class Planetas(db.Model):
    __tablename__="planetas"
    uid = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50),unique=True,nullable=False)
    population=db.Column(db.Integer,unique=True,nullable=False)
    terrain=db.Column(db.String(40),unique=True,nullable=True)
    
    def __repr__(self):
        return '<Planetas%r>' % self.name

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "population":self.population
            # do not serialize the password, its a security breach
        }
class FavPlanetas(db.Model):
    __tablename__="favplanetas"
    id = db.Column(db.Integer, primary_key=True)
    user=db.Column(db.String(120),db.ForeignKey('user.email'))
    planetas=db.Column(db.String(50),db.ForeignKey('planetas.name'))
    rel_user=db.relationship('User')
    rel_planetas=db.relationship('Planetas')
    def __repr__(self):
        return '<FavPlanetas %r>' % self.id

    def serialize(self):
        return {
            "uid": self.uid,
            "user": self.user,
            "planeta":self.planetas
            # do not serialize the password, its a security breach
        }