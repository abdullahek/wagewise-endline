from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_migrate import upgrade as upgrade_database
from glogic import app, db, prepare_app

prepare_app(environment='ms')
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
