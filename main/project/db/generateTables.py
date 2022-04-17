from project.db import db
from project.db.models import trends

def run():
    pass

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    run()