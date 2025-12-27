from . import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(162), nullable=False)


    def __repr__(self):
        return f'<User {self.login}>'
    
class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    article_text = db.Column(db.Text, nullable=False)
    is_favorite = db.Column(db.Boolean)
    is_public = db.Column(db.Boolean)
    lekes = db.Column(db.Integer, default=0)

    # Relationship removed: use login_id to reference author explicitly when needed

    def __repr__(self):
        # Avoid accessing related object directly in repr; use login_id for stability
        return f'<Article {self.title} by user_id={self.login_id}>'