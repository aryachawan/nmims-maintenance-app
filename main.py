from flask import Flask,render_template,redirect,request,session,url_for
import os
from dotenv import load_dotenv
from supabase import create_client

app = Flask(__name__)
app.secret_key = "Something"
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
admin_password=os.environ.get("ADMIN_PASSWORD")
admin_id=os.environ.get("ADMIN_ID")
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
    return render_template("index.html",otherclasslist=other_class_list)

@app.route("/complaint/<mode>",methods=["POST","GET"])
def complaint(mode):
    filename = ""
    inputimage = ""
    classtype = ""
    componentid = ""
    complaint = ""
    classnum = ""
    phase=""
    fileurl=""
    if request.method == "POST":
        if(request.form["flag"]=='uploadcomplaintrequest'):
            inputimage = request.files["inputimage"]
            filename = inputimage.filename
            classtype = request.form["classtype"]
            classnum = request.form["classnum"]
            componentid = request.form["componentid"]
            complaint = request.form["complaint"]
            phase=request.form['phase']
            if inputimage:
                inputimage.save(f"static/{filename}")
                filelink = f"static/{filename}"
                filetype = inputimage.filename.split(".")[-1]
                print(filetype)
                resp = supabase.storage.from_("maintenanceappimages").upload(filename,filelink,{"content-type":f"image/{filetype}"})
                fileurl = supabase.storage.from_("maintenanceappimages").get_public_url(filename)
                print(fileurl)
                #TEMP STORAGE IN SESSION 
                data={
                    "fileurl":fileurl,
                    "filename":filename,
                    "classtype":classtype,
                    "classnum":classnum,
                    "componentid":componentid,
                    "phase":phase,
                    "complaint":complaint
                }
                session['complaint_details']=data
        if(request.form['flag']=='uploadconfirmed'):
            data=session.get('complaint_details')
            fileurl=data['fileurl']
            filename=data['filename']
            classtype=data['classtype']
            classnum=data['classnum']
            componentid=data['componentid']
            phase=data['phase']
            complaint=data['complaint']
            response = supabase.table('maintenance_app').insert({"classroom":classtype+" "+classnum,"componentid":componentid,"complaint":complaint,"imageurl":fileurl,"phase":phase,"classtype":classtype,"filename":filename}).execute()
            return redirect(url_for("complaint",mode='confirmed'))
        if(request.form['flag']=='cancelupload'):
            data=session.get('complaint_details')
            filename=data['filename']
            supabase.storage.from_("maintenanceappimages").remove([filename])
            return redirect(url_for("complaint",mode='cancelled'))

    return render_template("upload.html",complaint=complaint,classnum=classnum,classtype=classtype,componentid=componentid,inputimagefilename=filename,otherclasslist=other_class_list,fileurl=fileurl,phase=phase,mode=mode)

@app.route("/admin",methods=["POST","GET"]) 
def admin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == admin_id and password == admin_password:
            passkey=os.environ.get("PASSKEY")
            return redirect(url_for("adminpanel",flag=passkey))
        else:
            return "Invalid Login Credentials"
    return render_template("adminlogin.html")
    

@app.route("/adminpanel/<flag>", methods=["POST", "GET"])
def adminpanel(flag):
    passkey = os.environ.get("passkey")
    if flag == passkey:
        if request.method == "POST":
            formflag = request.form.get("formflag")

            if formflag == "delcomplaint":
                complaintid = request.form["complaintid"]
                filename = request.form["filename"]
                supabase.table("maintenance_app").update({"completed": True}).eq("id", complaintid).execute()
                supabase.storage.from_("maintenanceappimages").remove([filename])
                return redirect(url_for("adminpanel", flag=passkey))

            elif formflag == "filter":
                classtype = request.form.get("classtype", "").strip()
                phase = request.form.get("phase", "").strip()

                query = supabase.table("maintenance_app").select("*").eq("completed", False)
                filters_applied = {}

                if classtype:
                    query = query.eq("classtype", classtype)
                    filters_applied["Class Type"] = classtype
                if phase:
                    query = query.eq("phase", phase)
                    filters_applied["Phase"] = phase

                session["comp_data"] = query.execute().data
                session["filters_applied"] = filters_applied  # Store applied filters
                session["tempflag"] = 11

            elif formflag == "removefilters":
                session.pop("comp_data", None)
                session.pop("filters_applied", None)
                session.pop("tempflag", None)
                return redirect(url_for("adminpanel", flag=passkey))

        compdata = session.get("comp_data") if session.get("tempflag") == 11 else supabase.table("maintenance_app").select("*").eq("completed", False).execute().data
        filters_applied = session.get("filters_applied", {})

        return render_template("admin.html", compdata=compdata, passkey=passkey, filters_applied=filters_applied)
    
    return "Login Attempt Failed"



    
if __name__ == "__main__":
    app.run(debug=True,port=5002)