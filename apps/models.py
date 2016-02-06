from apps import db

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255), primary_key = True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    joinDate = db.Column(db.DateTime(),default = db.func.now())
    level = db.Column(db.Integer, default = 0)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userEmail = db.Column(db.String(255), db.ForeignKey(User.email))
    user = db.relationship('User',backref=db.backref('articles', cascade='all, delete-orphan', lazy='dynamic'))
    content = db.Column(db.Text())

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userEmail = db.Column(db.String(255), db.ForeignKey(User.email))
    user = db.relationship('User', backref=db.backref('user_comments', cascade='all, delete-orphan', lazy='dynamic'))
    articleId = db.Column(db.Integer, db.ForeignKey(Article.id))
    article = db.relationship("Article", backref = db.backref('comments', cascade = 'all, delete-orphan'))
    content = db.Column(db.Text())
    dateCreated = db.Column(db.DateTime(), default = db.func.now())

