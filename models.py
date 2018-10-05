from settings import db


class Flow(db.Model):
    __tablename__ = 'flow'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    steps = db.relationship('Step', backref='flow', lazy=True, passive_deletes=True)

    def __repr__(self):
        return '<Flow {}>'.format(self.name)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'steps': [step.as_dict() for step in self.steps],
        }


class Step(db.Model):
    __tablename__ = 'step'
    id = db.Column(db.Integer, primary_key=True)
    flow_id = db.Column(db.Integer, db.ForeignKey('flow.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Step {}>'.format(self.name)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(db.Model):
     __tablename__ = 'user'
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(100), nullable=False)
     email = db.Column(db.String(120), nullable=False)
     password = db.Column(db.String(50), nullable=False)

     def __repr__(self):
         return '<User {}>'.format(self.username)

     def as_dict(self):
         return {
             'id': self.id,
             'username': self.username,
             'email': self.email,
             'password': self.password
         }



