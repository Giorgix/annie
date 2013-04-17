from annie import db


class User(db.Model):

    """
    unique identifier
    """
    user_id = db.Column(db.Integer, primary_key=True)

    """
    user name
    """
    user_name = db.Column(db.String, unique=True, nullable=False)

    """
    user password
    """
    user_password = db.Column(db.String(46), nullable=False)

    """
    user email
    """
    user_email = db.Column(db.String(255), nullable=False)

    def __init__(self, user_name, user_password, user_email):

        self.user_name = user_name
        self.user_password = user_password
        self.user_email = user_email

    def toJSON(self):
        return {
            "id":    self.user_id,
            "name":  self.user_name,
            "email": self.user_email,
        }

    def __repr__(self):
        return "<id: %d, name: %s, email: %s,>" % \
            (self.user_id, self.user_name, self.user_email)
