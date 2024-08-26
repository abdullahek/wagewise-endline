from datetime import datetime

from . import db


class User(db.Model):
    __tablename__ = "Data_for_G:Bot"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=False, unique=True)
    response = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, number, response):
        self.number = number
        self.response = response

class Question_List(db.Model):
    __tablename__ = "Question_List"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=False, unique=True)
    Question = db.Column(db.String(1000), nullable=False)
    Options = db.Column(db.String(4096), nullable=False)
    Status = db.Column(db.Boolean, nullable=False)
    Added_On = db.Column(db.DateTime, default=datetime.now)
    Options_List = db.Column(db.String(100), nullable=False)

    def __init__(self, number, response, Question, Options, Status, Added_On, Options_List):
        self.number = number
        self.response = response
        self.Question = Question
        self.Options = Options
        self.Status = Status
        self.Added_On = Added_On
        self.Options_List = Options_List

class User_Question_Logs(db.Model):
    __tablename__ = "User_Question_Logs"

    id = db.Column(db.Integer, primary_key=True)
    User_Number = db.Column(db.String(40), nullable=False, unique=True)
    Q_number = db.Column(db.String(20), nullable=False)
    Response_Status = db.Column(db.Boolean, nullable=False)
    Sent_On = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, User_Number, Q_number, Response_Status, Sent_On):
        self.User_Number = User_Number
        self.Q_number = Q_number
        self.Response_Status = Response_Status
        self.Sent_On = Sent_On

class User_Response_Logs(db.Model):
    __tablename__ = "User_Response_Logs"

    id = db.Column(db.Integer, primary_key=True)
    User_Number = db.Column(db.String(40), nullable=False, unique=True)
    Q_number = db.Column(db.String(20), nullable=False)
    Response = db.Column(db.String(20), nullable=False)
    Received_On = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, User_Number, Q_number, Response, Received_On):
        self.User_Number = User_Number
        self.Q_number = Q_number
        self.Response = Response
        self.Received_On = Received_On