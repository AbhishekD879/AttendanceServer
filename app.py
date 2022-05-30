import base64
# from crypt import methods
import dataBaseUtils
import bcrypt
from flask import Flask,jsonify, request,Response
from flask_cors import CORS, cross_origin
import io
from PIL import Image
from _03_facenet_keras import prepare_data
from _03_facenet_keras import face_recognizer_image
from _03_facenet_keras import utils
import pymongo
import os
import tensorflow as tf

tf.config.threading.set_intra_op_parallelism_threads(1)
# tf.config.threading.set_inter_op_parallelism_threads(2)
# path = "C:/AbhishekDiwate-Attendence_Cam/ServerFlask/data/people"
#
# file_count = len(os.listdir(path))
# print(file_count)
# prepare_data.prepareData()
client = pymongo.MongoClient("mongodb://PramodBorhade:9370300435@cluster0-shard-00-00.olibo.mongodb.net:27017,cluster0-shard-00-01.olibo.mongodb.net:27017,cluster0-shard-00-02.olibo.mongodb.net:27017/AttendenceDb?ssl=true&replicaSet=atlas-13dl2j-shard-0&authSource=admin&retryWrites=true&w=majority")
db=client.AttendenceDb
myColl=db["attendencs"]



# validAdmin=[
#     {
#         "email":"abhishekdiwate879gmail.com",
#         "pass":"abhishek"
#     }
#     ,
#     {
#         "email":"abhijeetthombare333@gmail.com",
#         "pass":"abhi@1234"
#     },
# ]


def people(name, images):
    
    people_dir = "data\people"
    j = 0
    names=[]
    for person_name in os.listdir(people_dir):
        names.append(person_name) 
    
    # img = base64.b64decode((str(images)))
    for image in images:
        img = base64.b64decode(image)
        j+=1
        path = os.path.join(people_dir, name)

        if name not in names:
            os.mkdir(path)
            names.append(name)
            path = os.path.join(people_dir, name)
        # img = Image.open(images)
            img1 = Image.open(io.BytesIO(img))
            paths = os.path.join(path, name + str(j))
            img1.save(paths + ".JPEG")
        path = os.path.join(people_dir, name)
        img1 = Image.open(io.BytesIO(img))
        paths = os.path.join(path, name + str(j))
        img1.save(paths + ".JPEG")

def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    # print(plain_text_password)
    #   (Using bcrypt, the salt is saved into the hash itself)
    a = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return a

app = Flask(__name__)
# app.config['CORS_HEADERS'] = 'application/json'
# CORS(app, support_credentials=True)
imagebase64 = ''


@app.route('/',methods=['GET'])
# @cross_origin(supports_credentials=True)
def home():
    return "Reached AttendanceCam Server"


@app.route('/addPeople',methods=['POST'])
def addpeople():
    if request.method=='POST':
       recivedData=request.get_json()
       query = request.args
       if(recivedData and query):
          people(query["name"],recivedData["image"])
          prepare_data.prepareData()
          return Response("valid")
       else:
          return Response("Invalid",status=404)

@app.route('/addUser',methods=['POST'])
def addUser():
    if request.method=='POST':
        userToBeAdded=request.get_json()
        
        query=request.args
        query=dict(query)
        if str(dict(db.myColl.find({'userName':  userToBeAdded['username']})))==str({}):
            if (userToBeAdded):
                if (len(userToBeAdded['username']) != 0 and len(userToBeAdded["password"]) != 0):
                    newUsertobeAddedObj = {
                        "userName": userToBeAdded['username'],
                        "passWord": get_hashed_password(userToBeAdded["password"]),
                        "classesConducted": []
                    }
                    data = myColl.insert_one(newUsertobeAddedObj)

                    if (data):
                        return "Data Added"
            else:
                return Response("Invalid", status=403)
        else:
            return Response("UserAlreadyExist",status=403)


@app.route('/authentication',methods=['POST'])
def auth():
    if request.method=='POST':
       recivedData=request.get_json()
       if(recivedData):
           # print(recivedData)
           if (dataBaseUtils.auth(recivedData["userCred"])):
               return "True"
           else:
               return "False"
       else:
          return Response("Invalid",status=404)

@app.route('/img', methods=['POST', 'GET'])
def base64I():
    if request.method == 'POST':
        # prepare_data.prepareData()
        base = request.get_json()
        if(base):
            imagebase64 = base["base64Img"]
            image = base64.b64decode(str(imagebase64))
            fileName = 'test.jpeg'
            imagePath = ('data/test/' + fileName)
            # imagePath = ('./imgDir/' + "test.jpeg")
            img = Image.open(io.BytesIO(image))
            img.save(imagePath, 'jpeg')
            # prepare_data.prepareData()
            reconizedStudents = face_recognizer_image.face_reconizer_image()
            
            dataTobeConvertedIntoPdf = dataBaseUtils.newClassUpdate(base["classDetails"], base["loggedUser"],
                                                                    reconizedStudents)

            # print(dataTobeConvertedIntoPdf,"oop")
            return jsonify(dataTobeConvertedIntoPdf)
        else:
            return Response("Invalid",status=404)




    elif request.method == 'GET':
        # alluser=myColl.find()
        # print(alluser[0])
        return "d"


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
