from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(votr, name='Dashboard')
admin.add_view(ModelView(Users, db.session))

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)