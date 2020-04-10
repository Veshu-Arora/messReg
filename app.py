from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super secret key"
DATABASE_URL = "postgres://rebcvzytadsgyg:07f08ad498ca6b6f4b396b0053ba715cd0b2749846db3ae71424e5282944ea4c@ec2-52-200-119-0.compute-1.amazonaws.com:5432/d4hmsbipbinjua"

# Set up database
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))


course = {
    '1' : 'B.Tech',
    '2' : 'M.Sc.',
    '3' : 'B.Sc',
    '4' : 'B.Pharma',
    '5' : 'M.A.Yoga',
    '6' : 'B.com'
} 


month = {
    '1'  : 'January',
    '2'  : 'February',
    '3'  : 'March',
    '4'  : 'April',
    '5'  : 'May',
    '6'  : 'June',
    '7'  : 'July',
    '8'  : 'August',
    '9'  : 'September',
    '10' : 'October',
    '11' : 'November',
    '12' : 'December'
}


@app.route("/transaction")
def transaction():
    result = db.execute("SELECT * FROM messfee").fetchall()
    return render_template('transaction.html', result = result)

@app.route("/students")
def students():
    result = db.execute("SELECT * FROM student").fetchall()
    return render_template('students.html', result = result)    

# This route will render enter.html
@app.route("/")
@app.route("/enter")
def enter():
    return render_template('enter.html', course = course)


@app.route("/savedata",methods=["POST"])
def savedata():
    full_name = request.form.get('FullName')
    phone = request.form.get('Phone')
    room = request.form.get('Room')
    year = request.form.get('Year')
    course_id = request.form.get('Course_id')
    course_name = course[course_id]
    
    db.execute("INSERT INTO student(full_name, room, course_name, year, phone) VALUES(:full_name, :room, :course_name, :year, :phone)",
    {"full_name":full_name,"room":room,"course_name":course_name,"year":year,"phone":phone})
    db.commit()
    db.close()
    flash("Data is submitted successfully")
    return redirect(url_for('enter'))   



@app.route("/payfees")
def payfees():
    return render_template('payfees.html', month = month)

# This route will have login credintials and will validate from database
@app.route("/feesrecord", methods = ['POST'])
def feesrecord():
    student_phone = request.form.get('Phone')
    fees_paid = request.form.get('Fees')
    fees_due = 3000-int(fees_paid)
    month_id = request.form.get('month_id')
    month_name = month[month_id]
    result = db.execute("SELECT * FROM student WHERE phone=:phone",
        {"phone":student_phone}).fetchall()

    for r in result:
        student_name = r.full_name 
        student_room = r.room

    now = datetime.now()
    paying_date = now.strftime("%d/%m/%y")
    paying_time = now.strftime("%H:%M:%S")

    if result == []:
        return "Invalid email or password"
    else:

        db.execute("INSERT INTO messfee(student_phone, student_name, room, paying_date, paying_time, month, fees_paid, fees_due) VALUES(:phone_std, :full_name, :room, :paying_date, :paying_time, :month, :fees_paid, :fees_due)",
        {"phone_std":student_phone,"full_name":student_name,"room":student_room,"paying_date":paying_date,"paying_time":paying_time,"month":month_name,"fees_paid":fees_paid,"fees_due":fees_due})
        db.commit()
        db.close()
        flash(f"Your Fees has been paid successfully { student_name }")
        return redirect(url_for('payfees'))



    #resulttemp = db.execute("SELECT * FROM messfee WHERE fees_due != 0").fetchall()

    #for m in resulttemp:
        #print(f"Due fees unpaid for month {m.month}")
    #return "success"    
        


@app.route("/paydue")
def paydue():
    return render_template('paydue.html', month = month)

@app.route("/updatedue",methods=["POST"])
def updatedue():
    #now = datetime.now()
    #paying_time = now.strftime("%H:%M:%S")
    student_phone = request.form.get('Phone')
    due_paid = request.form.get('Due')

    result = db.execute("SELECT * FROM messfee WHERE student_phone=:phone AND fees_due != 0",
    {'phone':student_phone}).fetchall()
    for r in result:
        previous_due = r.fees_due
        due_month = r.month
        previous_fees = r.fees_paid
        student_name = r.student_name
    updated_due = previous_due - int(due_paid) 
    updated_fees =  previous_fees + int(due_paid)   

    db.execute("UPDATE messfee SET fees_due=:new_due ,fees_paid=:new_fees WHERE student_phone=:phone AND month=:month",
            {"phone":student_phone, "new_due":updated_due, "month":due_month, "new_fees":updated_fees})
    db.commit()
    db.close()
    flash (f"Your Due Fees has been updated successfully { student_name }. Now your remaining due fees is { updated_due } Rupees") 
    return redirect(url_for('paydue'))        


#@app.route("/getinfo/<number>")
#def encryption(number):

    #result = db.execute("SELECT * FROM hostel WHERE phoneNo=:phone",
    #{"phone":number}).fetchall()
    #db.commit()
    #db.close()

    #for r in result:
     #   name = r.full_name
      #  mother =r.mother
       # father =r.father
        #email = r.email
        #password = r.password

    #response = {
     # "Full Name": name,
      #"Mother Name": mother,
      #"Father Name": father,
      #"Email Address": email,
      #"Password": password}

    
    
    #return jsonify(response)

#def register():
 #   return render_template('register.html')

#@app.route("/visitors")
#def visitors():
 #   guest = db.execute("SELECT * FROM guest").fetchall()
  #  hostel = db.execute("SELECT * FROM hostel").fetchall()
   # return render_template('visitors.html', guest = guest, hostel = hostel )



# This route will render login.html
      

# This route will have signup credintials and will submit in database
      

#@app.route("/updatetime/<guest_id>",methods=["GET"])
#def updatetime(guest_id):
 #   now = datetime.now()
  #  leaving_time = now.strftime("%H:%M:%S")
   # db.execute("UPDATE guest SET leaving_time=:leaving_time WHERE id=:guest_id",
    #        {"guest_id":guest_id, "leaving_time":leaving_time})
    #db.commit()
    #db.close()
    #return redirect(url_for('visitors'))
# This route will render login.html
#@app.route("/show")
#def show():
    #results = db.execute("SELECT * FROM userData").fetchall()
    #return render_template('show.html',results=results)

# This route will render login.html
#@app.route("/delete/<string:key_id>",methods=["GET"])
#def delete(key_id):
    #db.execute("DELETE FROM userData WHERE id=:id",
        #{"id":key_id})
    #db.commit()
    #db.close()
    #return "Successfully deleted the account"

#@app.route("/update/<string:key_id>", methods=['GET'])
#def update(key_id):
    #db.execute("UPDATE userData SET full_name = 'ULLU' WHERE id=:id",
       #{"id":key_id})
   #db.commit()
    #db.close()
    #return "successfuly updated the name"

# This route will render signup.html
#@app.route("/updateform/<string:key_id>", methods=['GET'])
#def updateform(key_id):
    #return render_template('update.html',key_id=key_id)  

#@app.route("/updatev/", methods=['GET'])
#def updatev():
    #key_id = request.args.get('key_id')
    #new_pass = request.args.get('password')
    #c_new_pass = request.args.get('confirm password')
    
    #if(new_pass == c_new_pass):
        #db.execute("UPDATE userData SET password=:password WHERE id=:id",
            #{"id":key_id, "password":new_pass})
        #db.commit()
        #db.close()
        #return f"successfully updated the pasword"    


if __name__ == "__main__":
     app.run(debug = True)
   