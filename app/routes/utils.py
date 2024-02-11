from flask import session

def is_logged():
    return "user" in session.keys()

def is_man(gender):
    if(gender != 'man'):
        return False
    else:
        return True

def is_nice(number):
    return number == 69
