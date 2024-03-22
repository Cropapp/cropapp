import streamlit as st
import re
import sqlite3
import pandas as pd

conn = sqlite3.connect('data.db')
c = conn.cursor()
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,email TEXT,Password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,City,email,Password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,email,Password,Cpassword) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,City,email,Password,Cpassword))
    conn.commit()
def login_user(email,Password):
    c.execute('SELECT * FROM userstable WHERE email =? AND Password = ?',(email,Password))
    data = c.fetchall()
    return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def delete_user(Email):
    c.execute("DELETE FROM userstable WHERE Email="+"'"+Email+"'")
    conn.commit()

choice = st.sidebar.selectbox("home page:",
                     ['Home','Signup','Login','Contact us'])

if choice == 'Home':
    st.title("Crop Recommendation")
    st.text("This webapp recommends the best crop to plant on soil and weather conditions!")
if choice == 'Signup':
    FirstName = st.text_input("FIRST NAME")
    LastName = st.text_input("LAST NAME")
    Mobile = st.text_input("MOBILE NUMBER")
    City = st.text_input("City")
    email = st.text_input("EMAIL")
    Password = st.text_input("PASSWORD",type="password")
    Cpassword = st.text_input("CONFIRM PASSWORD",type="password")
    b2 = st.button('Signup')
    if b2:
        pattern=re.compile("(0|91)?[7-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if Password==Cpassword:
            if (pattern.match(Mobile)):
                if re.fullmatch(regex, email):
                    create_usertable()
                    add_userdata(FirstName,LastName,Mobile,City,email,Password,Cpassword)
                    st.success("SignUp Success")
                    st.info("Go to Logic Section for Login")
                else:
                    st.warning("Not Valid Email")         
            else:
                st.warning("Not Valid Mobile Number")
        else:
            st.warning("Pass Does Not Match")
if choice == 'Login':
    email=st.sidebar.text_input("EMAIL")
    Password=st.sidebar.text_input("PASSWORD",type="password")
    if st.sidebar.checkbox('login'):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, email):
            result = login_user(email,Password)
            if result:
                if email== 'a@a.co':
                    st.success("Logged In as {}".format(email))
                    demail=st.text_input("Enter Delete EMAIL")
                    if st.button("Delete"):
                        delete_user(demail)
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","City","Email","Password","Cpassword"])
                    st.dataframe(clean_db)
                else:
                    st.success("Logged In as {}".format(email))
                    choice3 = st.selectbox("Select ML:",
                                         ["SVM","NB","KNN","DT","RF","ET"])
                    
                    import pickle
                    model=pickle.load(open("model_iris.pkl","rb"))
                    sl=float(st.slider("Enter Sepal_length=",5.0))
                    sw=float(st.slider("Enter Sepal_width=",5.0))
                    pl=float(st.slider("Enter Petal_length=",5.0))
                    pw=float(st.slider("Enter Petal_width=",5.0))
                    if st.button('Predict'):
                        if choice3=="SVM":
                            st.success(model[0].predict([[sl,sw,pl,pw]]))
                        if choice3=="NB":
                            st.success(model[1].predict([[sl,sw,pl,pw]]))
                        if choice3=="KNN":
                            st.success(model[2].predict([[sl,sw,pl,pw]]))
                        if choice3=="DT":
                            st.success(model[3].predict([[sl,sw,pl,pw]]))
                        if choice3=="RF":
                            st.success(model[4].predict([[sl,sw,pl,pw]]))
                        if choice3=="ET":
                            st.success(model[5].predict([[sl,sw,pl,pw]]))
            else:
                st.warning("Incorrect Email/Password")
        else:
            st.warning("Not Valid Email")       
if choice == 'Contact us':
    st.text("NAME:- KESHA SHAH")
    st.text("EMAIL ID:- keshashah1666@gmail.com")
    st.text("ADDRESS:- NEW VIP ROAD,VADODARA")
    
