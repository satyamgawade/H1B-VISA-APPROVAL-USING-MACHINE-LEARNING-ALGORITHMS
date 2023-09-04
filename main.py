from flask import Flask, render_template, request
import pickle
import numpy as np
import db_function as db
import exceptionhandling as exph


app = Flask(__name__)

# for converting user inputed employer_name into required format
file1 = open('le_emp_name.pkl', 'rb')
le_emp_name = pickle.load(file1)

# for converting user inputed soc_name into required format
file2 = open('le_soc_name.pkl', 'rb')
le_soc_name = pickle.load(file2)

# for converting user inputed worksite into required format
file3 = open('le_worksite.pkl', 'rb')
le_worksite = pickle.load(file3)

# for converting user inputed scaling object for scaling the salary into required format
file4 = open('s_sc.pkl', 'rb')
s_sc = pickle.load(file4)

# importing the xg boost model
file5 = open('model_xgb.pkl', 'rb')
model_xgb = pickle.load(file5)


def transform(x):
    # Function which transforms the user input into an array or numeric values for predicting
    x=np.array([x])
    x[:,0] = s_sc.transform([x[:,0]])
    x[:,1] = 1 if (x[:,1]) == 'Y' else 0
    x[:,2] = le_emp_name.transform(x[:,2])
    x[:,3] = le_soc_name.transform(x[:,3])
    x[:,4] = le_worksite.transform(x[:,4])
    x = x.astype(float)
    return x


# @app.route("/", methods=["GET"])
# def root():
#    return render_template("index.html")
    

@app.route("/", methods=["GET", "POST"])
def signup_home():
    return render_template("signup.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    email, psw, psw_repeat = request.form.get("email"), request.form.get('psw'), request.form.get("psw-repeat")
    print(email, psw, psw_repeat)
    if psw == psw_repeat:
        db.new_user_signup(email, psw)
        return render_template("signin.html")
    else:
    	return f'<h3>Sorry {email}, the Password was Incorrect.</h3> <br> <a href="/"> <button type="button">Signup</button> </a>'

@app.route("/signin", methods=["GET", "POST"])
def signin_home():
    return render_template("signin.html")

@app.route("/signedin", methods=["GET", "POST"])
def signed_in():
    return render_template("index.html")
    
@app.route("/predict", methods=['GET', 'POST'])
def predict_acceptance():
    x = (float(request.form.get("prevailing_wage")), 
         request.form.get('full_time'), 
         request.form.get("employer_name"), 
         request.form.get("soc_name"), 
         request.form.get("worksite"))
    
    try:
        if float(request.form.get("prevailing_wage")) == 0:
            x = transform(x)
            predictions = "CERTIFIED" if model_xgb.predict(x)[0] == 1 else "DENIED"
    
            param=[{'wages':request.form.get("prevailing_wage"),
                    'full_time': request.form.get('full_time'), 
                    'employer':request.form.get("employer_name"), 
                    'soc':request.form.get("soc_name"), 
                    'worksite':request.form.get("worksite"), 
                    'prediction':predictions}]
            
            return render_template("invalidwage.html", param=param)
            # raise exph.ZeroWageError
        else:
            x = transform(x)
            predictions = "CERTIFIED" if model_xgb.predict(x)[0] == 1 else "DENIED"
    
            param=[{'wages':request.form.get("prevailing_wage"),
                    'full_time': request.form.get('full_time'), 
                    'employer':request.form.get("employer_name"), 
                    'soc':request.form.get("soc_name"), 
                    'worksite':request.form.get("worksite"), 
                    'prediction':predictions}]
            return render_template("test_withoutdb.html", param=param)
            
    except exph.ZeroWageError:
        print("Wage Entered is Zero and Invalid, Please try again")
            

app.run(debug=True)