import pymongo
import bcrypt

client = pymongo.MongoClient("mongodb://PramodBorhade:9370300435@cluster0-shard-00-00.olibo.mongodb.net:27017,cluster0-shard-00-01.olibo.mongodb.net:27017,cluster0-shard-00-02.olibo.mongodb.net:27017/AttendenceDb?ssl=true&replicaSet=atlas-13dl2j-shard-0&authSource=admin&retryWrites=true&w=majority")
db=client.AttendenceDb
mycol=db["attendencs"]

def check_password(plain_text_password, hashed_password):
    hashed_password=hashed_password.decode("utf-8") 
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))

def newClassConducted(classDetail,Subject,date,lectureNo,students):
    newclass={
        "classDetail":classDetail,
        "Subject":Subject,
       "date":date,
        "lectureNo":lectureNo,
        "students":students
    }
    return newclass

def auth(recivedData):

    found=mycol.find_one({"userName": recivedData["username"]})
    # print(found)
    if (found):
        authStatus =check_password(recivedData["password"], found["passWord"])
        if authStatus:
            return True
        else:
            return False

def newClassUpdate(classDetails,loggedUser,reconizedStudents):
    if(len(reconizedStudents)!=0):
        
        newclass = {
            "classDetail": classDetails['className'],
            "Subject": classDetails['subject'],
            "date": classDetails['date'],
            "lectureNo": classDetails['lecture'],
            "students": reconizedStudents
        }
        data = mycol.find_one({"userName": loggedUser["username"]})
        # print(data)
        up = data['classesConducted']
        updated = mycol.update_one(data, {"$set": {"classesConducted": up + [newclass]}})
        # print(updated)

        return (newclass,loggedUser)






