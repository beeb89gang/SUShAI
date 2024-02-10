from flask import Flask, session

def is_logged():
    return "user" in session.keys()

def is_man(gender):
    if(gender != 'man'):
        print("go back in the kitchen")
        return False
    else:
        return True

def is_nice(number):
    return number == 69
