# import flask and its components
from flask import *
import os

# create a flask application and give it a name
app = Flask(__name__)

# configure the location to where your product images will be saved on your application
app.config["UPLOAD_FOLDER"] ="static/images"

# import the pymysql model - it helps us to create a connection between python flask and nysql database
import pymysql


# below is a sign up route
@app.route("/api/signup", methods = ["POST"])
def signup():
    if request.method == "POST":
        # extract the different details entered on the form
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]

        # by use of the print function lets print all those details sent with the upcoming request
        # print(username, email, password, phone)

        # establish connection between flask/python and mysql
    connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")
        # create a cursor to execute the sql queries
    cursor = connection.cursor()

        # structure an sql to insert the details received from the form
        # %s is a placeholder -> A placeholder stands in places of actual values i.e we shall replace them later on
    sql = "INSERT INTO users(username,email,phone,password) VALUES(%s, %s, %s, %s)"

        # create a tuple that will hold all the data goten from the form
    data = (username, email, phone, password)

        # by use of the cursor execute the sql as you replace the placeholders with actual values
    cursor.execute(sql, data)

        # commit the changes to the database
    connection.commit()

    return jsonify({"message" : "User registered successfully"})


# below is a login/sign in route
@app.route("/api/signin", methods=["POST"])
def signin():
    if request.method == "POST":
        # extract the two details entered on the form
        email=request.form["email"]
        password=request.form["password"]

        # print out the details entered
        # print(email, password)

        # create /establish a connection to the database
        connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

        # create a cursor
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # structure the sql query that will check whether the email and the password entered are correct
        sql = "SELECT * FROM users WHERE email = %s AND password = %s"

        # put the data recieved from the form into a tuple
        data = (email, password)

        # by use if the cursor execute the sql
        cursor.execute(sql, data)

        # check whether there are rows returned and store them in a variable
        count = cursor.rowcount

        # if there are recordss returned it means the password and the email are correct otherwise it means they are wrong
        if  count == 0:
            return jsonify({"message" : "Login failed"})
        else:
            # there must be a user so we create a variable that will hold the details of the userf fetched from the database
            user = cursor.fetchone()
            # return the details to the frontend as weel as a message
            return jsonify({"message" : "user Logged in successfully", "user":user})


# below is the route for adding products
@app.route("/api/add_product", methods = ["POST"])
def Addproducts():
    if request.method == "POST":
        # extract the data entered on the form
        product_name = request.form["product_name"]
        product_description = request.form["product_description"]
        product_cost = request.form["product_cost"]
        # for the product photo we shall fetch it from files as shown below
        product_photo = request.files["product_photo"]

        # extract the file name of the product photo
        filename = product_photo.filename
        # by use of the os module we can extract the file path where the image is currently saved
        photo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # save the product photo image into the new location
        product_photo.save(photo_path)

        # print them out to test whether you are receiving the details sent with the request.
        # print(product_name, product_description, product_cost, product_photo)

        # establish a connection to the db
        connection=pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

        # create a cursor
        cursor=connection.cursor()

        # structure an sql query to insert the product details to the database
        sql = "INSERT INTO product_details(product_name, product_description, product_cost, product_photo) VALUES (%s, %s, %s, %s)"

        # create the tuple that will hold the data from the form which are currently being held on different variables declaired.
        data = (product_name, product_description, product_cost, filename)
        # use the cursor to execute the sql as you replace the placeholders with actual data.
        cursor.execute(sql, data)

        # commit the changes to the database
        connection.commit()



        return jsonify({"message" : "Product added successfully"})




# run the application
app.run(debug=True)