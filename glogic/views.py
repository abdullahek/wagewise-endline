from . import app
from . import bot_view
from flask import request


@app.route('/', methods=['GET', 'POST'])
def root():
    print(request)
    return "I'm working"
