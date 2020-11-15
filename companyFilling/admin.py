from flask_admin.contrib.sqla import ModelView


class MyModelView(ModelView):
    def is_accessible(self):
        return True

