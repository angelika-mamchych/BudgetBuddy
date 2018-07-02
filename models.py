from app import db


class Flow(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    flowname = db.Column(db.String(100), nullable=False)
    stepname1 = db.Column(db.String(100), nullable=False)
    stepname2 = db.Column(db.String(100), nullable=False)
    stepname3 = db.Column(db.String(100), nullable=False)
    steptype1 = db.Column(db.String(100), nullable=False)
    steptype2 = db.Column(db.String(100), nullable=False)
    steptype3 = db.Column(db.String(100), nullable=False)
    amount1 = db.Column(db.Float, nullable=False)
    amount2 = db.Column(db.Float, nullable=False)
    amount3 = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Flow {}>'.format(self.flowname)