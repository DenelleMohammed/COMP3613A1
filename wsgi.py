import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models.Driver import Driver
from App.models.Resident import Resident
from App.models import (User, Drive, Stop)
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from datetime import datetime


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("user_type", default="resident") #, help="Type of user: resident or driver")
@click.argument("status", default="active") # help="Driver status")
@click.argument("street_id", default=1) # type=int, help="Street ID")
def create_user_command(username, password, user_type, status, street_id):
    create_user(username, password, user_type = user_type, status = status, street_id = street_id)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
COMP 3613 Assignment 1 Commands; Bread Van App
'''
driver_cli = AppGroup('driver', help='Driver object commands')

@driver_cli.command("schedule-drive", help="Schedule a drive for a driver") # flask driver schedule-drive 2 20 2025-10-15 14:30
@click.argument("driver_id", type=int)
@click.argument("street_id", type=int)
@click.argument("date")
@click.argument("time")
def schedule_drive_command(driver_id, street_id, date, time):
    driver = Driver.query.filter_by(driver_id=driver_id).first()
    if not driver:
        print(f"No driver found with ID {driver_id}")
        return
    
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    time_obj = datetime.strptime(time, "%H:%M").time()
    datetime_obj = datetime.combine(date_obj, time_obj)
    new_drive = driver.schedule_drive(driver_id, street_id, datetime_obj)
    print(f"Scheduled drive: {new_drive}")

@driver_cli.command("view-drives", help="View all drives for a driver")
@click.argument("driver_id", type=int)
def view_drives_command(driver_id):
    driver = Driver.query.filter_by(driver_id=driver_id).first()
    if not driver:
        print(f"No driver found with ID {driver_id}")
        return
    
    drives = driver.drives
    if not drives:
        print(f"No drives found for driver ID {driver_id}")
        return
    
    for drive in drives:
        print(drive)

app.cli.add_command(driver_cli)

resident_cli = AppGroup('resident', help='Resident object commands') # flask resident view_inbox 10
@resident_cli.command("view-inbox", help="View inbox for a resident")
@click.argument("resident_id", type=int)
def view_inbox_command(resident_id):
    resident = Resident.query.filter_by(resident_id = resident_id).first()

    if not resident:
        print(f"No resident found with ID {resident_id}")
        return
    
    drive = resident.view_inbox(resident.street_id)
    print(f"Drives for street ID {resident.street_id}:")
    if not drive:
        print(f"No drives found for street ID {resident.street_id}")
        return
    for d in drive:
        print(d)

@resident_cli.command("request-stop", help="Request a stop from a driver") # flask resident request-stop 1 10
@click.argument("drive_id", type=int)
@click.argument("street_id", type=int)
def request_stop_command(drive_id, street_id):
    resident = Resident.query.filter_by(street_id=street_id).first()
    if not resident:
        print(f"No resident found for street ID {street_id}")
        return
    stop = resident.request_stop(resident.resident_id, drive_id, street_id)
    if stop:
        print(f"Stop requested: {stop}")
    else:
        print("Failed to request stop.")

@resident_cli.command("view-driver", help="View driver details") # flask resident view-driver 2 10
@click.argument("driver_id", type=int)
@click.argument("resident_id", type=int)
def view_driver_command(driver_id, resident_id):
    resident = Resident.query.filter_by(resident_id=resident_id).first()
    driver = Driver.query.filter_by(driver_id=driver_id).first()
    if not driver:
        print(f"No driver found with ID {driver_id}")
        return
    
    print(resident.view_driver(driver_id))

app.cli.add_command(resident_cli)


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)