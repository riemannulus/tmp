from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = db.Table(
    'user_place_association',
    db.Column(
        'users',
        db.String(40),
        db.ForeignKey('users.ip'),
        primary_key=True
    ),
    db.Column(
        'places',
        db.String(40),
        db.ForeignKey('places.code')
    )
)


class User(db.Model):
    __tablename__ = 'users'

    ip = db.Column(db.String(40), primary_key=True)
    places = db.relationship(
        'Place',
        secondary=association_table,
        back_populates='users'
    )


class Place(db.Model):
    __tablename__ = 'places'

    code = db.Column(db.String(40), nullable=False, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    users = db.relationship(
        'User',
        secondary=association_table,
        back_populates='places'
    )


class Matrix(db.Model):
    __tablename__ = 'matrix'

    ip = db.Column(db.String(40), db.ForeignKey('users.ip'), primary_key=True)
    choice = db.Column(db.String(10), nullable=False)
    user = db.relationship("User", backref=db.backref('matrix', lazy=True))
