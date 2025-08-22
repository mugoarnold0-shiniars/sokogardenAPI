from flask import *
import os

# import pymySQL that will enable you to create a connection btwn vscode and the db(SQL)
import pymysql
import pymysql.cursors


# create a web app
app= Flask(__name__)

# configure the upload folder(where the files are stored)
app.config["UPLOAD_FOLDER"] = "static/images"


# below is the sign up route (regestration)
@app.route("/api/signup",methods=["POST"])
def signup():
    if request.method == "POST":
        # extract different details entered on the form
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        phone = request.form["phone"]


        # print("The inserted details are:",(username,password,email,phone))
        # create/establish a connection to the database

        connection =pymysql.connect(host="localhost",user="root",password="",database="sokogarden")


        # create a cursor
        cursor = connection.cursor()

        # structure a SQL query to insert data into the table
        sql = "INSERT INTO `users`(`username`, `password`, `email`, `phone`) VALUES (%s,%s,%s,%s)"

        # put the data ito a tuple
        data = (username,password,email,phone)

        # use the cursor to execute the SQL as you replace the placeholder with actual data
        cursor.execute(sql,data)

        # commit the changes into the database
        connection.commit()

        return jsonify({"message":"user registered successfully"})
    


@app.route ("/api/signin",methods=['POST'])
def signin():
    if request.method == "POST" :
        email = request.form ["email"]
        password = request.form ["password"]
            
        # print("the inserted emai and password is:",(email,password))

        # create a connection to the db
        connection = pymysql.connect (host="localhost",user="root",password="",database="sokogarden")
        # create a cursor
        cursor= connection.cursor(pymysql.cursors.DictCursor)

        # structure an sql for login in
        sql = "SELECT * FROM users WHERE email =%s AND password=%s"

        # create a tuple
        data = (email,password)

        # use the cursor to execute the sql as u replace the placeholder with actual data
        cursor.execute(sql,data)

        # check whether there is a user being retured based on the inserted email and password 
        # if there is a user,  the number or rows are more than one
        # if there is no user,the number of rows is zero
       



        if cursor.rowcount == 0:
            return jsonify({"message":"Login failed.Please try again"})
        else :
            # when yhe details are correct create a variable called user and store the details of the user in the variables
            # then return a success message
            user = cursor.fetchone()

            return jsonify({"message":"Login succesful","user":user})
        



@app.route("/api/addproduct", methods=["POST"])
def addproduct():
    if request.method == "POST" :
        # extract details from the keys on the form and store them into variables
        product_name = request.form ["product_name"]
        product_description = request.form ["product_description"]
        product_cost = request.form["product_cost"]

        # the product photo we shall request it from files
        product_photo = request.files["product_photo"]
        # extract the file name of the photo
        filename = product_photo.filename
        # by use of the os(Operating System)take the path of the photo
        photo_path = os.path.join(app.config["UPLOAD_FOLDER"],filename)
        # save your photo on that particular path
        product_photo.save(photo_path)
        # print("the details are:",(product_name,product_description,product_cost,photo_path))
        connection =pymysql.connect(host="localhost",user="root",password="",database="sokogarden")
        cursor =connection.cursor()
        sql = "INSERT INTO product_details(product_name,product_description,product_cost,product_photo)VALUES(%s,%s,%s,%s)"
        data = (product_name,product_description,product_cost,filename)
        cursor.execute (sql,data)
        connection.commit()


        return jsonify({"message":"product added successful"})
    



@app.route("/api/getproduct",methods=["GET"])
def getProduct():
        # establish a connection to the db
        connection = pymysql.connect(host="localhost",database="sokogarden",user="root",password="")
        # create a cursor
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        # structure the sql
        sql ="select*from product_details"

        # use the cursor to execute sql 
        cursor.execute(sql)
        # create a variable that will hold all the products fetched from te db
        product = cursor.fetchall()
        # then return the product as the response
        
        return jsonify(product)

        # return jsonify({"Messagge":"Get product accessed"})
# run the web
app.run(debug=True)