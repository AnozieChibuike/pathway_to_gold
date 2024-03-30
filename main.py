from app import app, db

from app.models.users import Users

@app.shell_context_processor
def make_shell_context():
    return {'db': db,'Users':Users}
