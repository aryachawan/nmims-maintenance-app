from flask import Flask,render_template,redirect,request
import os
from dotenv import load_dotenv
from supabase import create_client

app = Flask(__name__)
app.secret_key = "Something"
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url,key)
other_class_list = my_list = [
    "Automation Lab",
    "Pneumatic Lab",
    "AR/VR LAB",
    "Sensor IOT Lab",
    "Library",
    "Hydraulics Lab",
    "Boys Common Room",
    "Girls Common Room",
    "Hardware Lab 1",
    "Hardware Lab 2",
    "Hardware Lab 3",
    "Dean Office",
    "Physics Lab",
    "DE Lab",
    "ES Lab",
    "Advance Communication Lab",
    "Basic Communication Lab",
    "AI LAB",
    "Robotics Lab",
    "Additive Manufacturing Lab",
    "Placement Office",
    "Admin Department",
    "Conference Room",
    "Exam 1",
    "Exam 2",
    "Exam 3",
    "AMU ROOM 1",
    "Mini Auditorium",
    "V.C. Room 1",
    "V.C. Room 2"
]

@app.route("/",methods=["POST","GET"])
def home():
    filename = ""
    inputimage = ""
    classtype = "CR"
    componentid = ""
    complaint = ""
    classnum = ""
    if request.method == "POST":
        inputimage = request.files["inputimage"]
        filename = inputimage.filename
        classtype = request.form["classtype"]
        classnum = request.form["classnum"]
        componentid = request.form["componentid"]
        complaint = request.form["complaint"]
        print(filename,classtype,classnum,componentid,complaint)
        if inputimage:
            inputimage.save(f"static/{filename}")
            
    return render_template("index.html",complaint=complaint,classnum=classnum,classtype=classtype,componentid=componentid,inputimagefilename=filename,inputimage=inputimage,otherclasslist=other_class_list)

if __name__ == "__main__":
    app.run(debug=True,port=5002)