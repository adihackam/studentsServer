import json
import os 
from flask import Flask, request 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

myFile= "./back/students.json"
students={}

def loadFromFile():
    isExist = os.path.exists(myFile)
    if isExist:
        with open(myFile, 'r') as openFile:
            students = json.load(openFile)
        return students
    return []

def save2File(students):
    jsonString = json.dumps(students, indent=4)
    with open(myFile, "w") as outfile:
	    outfile.write(jsonString)


@app.route('/students', methods = ['GET', 'POST','DELETE'])
@app.route('/students/<id>', methods = ['GET', 'POST','DELETE','PUT'])
def crude_students(id=-1):
    if request.method == 'POST':
        request_data = request.get_json()
        name= request_data["name"]
        email = request_data["email"]
        grade = request_data['grade']
        subject = request_data['subject']

        students = loadFromFile() 
        maxId = 0
        for stu in students:
            if stu['id'] > maxId : 
                maxId = stu['id']
        newStudent = {"id":maxId + 1, "name": name, "email": email, "grade": grade, "subject": subject}
        students.append(newStudent)
        save2File(students)
        return {"msg":"new student was added"} 


    if request.method == 'GET':
        res=[]
        students = loadFromFile() 
        for student in students:
            res.append({"name":student['name'],"id":student['id'],"email":student['email'], "grade":student['grade'], "subject":student['subject']})
        return  res
        # return  (json.dumps(res))
    if request.method == 'DELETE': 
        students = loadFromFile() 
        for stu in students:
            if stu['id'] == int(id): 
                students.remove(stu)
        save2File(students)
        return {"msg":"row deleted"}

    if request.method == 'PUT':
        request_data = request.get_json()
        students = loadFromFile() 
        for stu in students:
            if stu['id'] == int(id): 
                stu['email'] = request_data['email']
                stu['grade'] = request_data['grade']
                stu['name']= request_data['name']
                stu['subject']= request_data['subject']
        save2File(students)
        return {"msg":"student updated"}

@app.route('/')
def about():
    return 'aaaa'

# def index():
#     return render_template('index.html')
 
if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug = False)