from audioop import avg
import py_compile
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy import func


app = Flask(__name__)

# inform Flask app which database to work with
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres123#@localhost/height-collector'

# create a SQLAlchemy object for the Flask app
db = SQLAlchemy(app)

#from SQLAlchemy object access the model class, so the SQLAlchemy object is inheriting from model class of the SQLAlchemy object
class Data( db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    height = db.Column(db.Integer)

    # Initialize the instance variables, this method is the first to be excuted when you call the class instance
    def __init__(self, email, height):
        self.email = email
        self.height = height


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/sucess', methods=['POST'])
def sucess():
    if request.method == 'POST':
        email = request.form['email_name']
        height = request.form['height_name']
        # create an object instance of the data class
        data = Data(email,height)

        if not bool(db.session.query(Data).filter_by(email=email).first()):
            #data to the column fields 
            db.session.add(data)
            db.session.commit()
            #Create a average height variable and convert it to a number using the .scalar method.
            average_height=db.session.query(func.avg(Data.height)).scalar()
            average_height=round(average_height,1)
            count=db.session.query(Data.height).count()
            send_email(email,height,average_height,count)
            return render_template("sucess.html")
    
    return render_template("index.html", text = "Seems like we've have received data from the address entered")


if __name__ == '__main__':
    app.debug = True
    app.run()
