from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

from app import app
""" import app == import "app" in __init__.py """
from app.db import conn
from app.query import show_account
from app.form import LoginForm, RegisterAccountForm, RegisterPersonalInfoForm

role = -1
account_id = -1
""" init global values """


@app.route('/')
def show_main_page():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global role, account_id

    username = request.form.get('username')
    password = request.form.get('login_pass')
    cur = conn.cursor()
    cur.execute("select password_hash, account_id from loginInfo where "
        "login_name = "+"\'"+username+"\';")
    record = cur.fetchone()
    """ record = [password_hash, acc_login]"""

    if not check_password_hash(record[0], password):
        flash('Invalid username of password! ')
        return redirect(url_for('show_main_page'))
    else:
        cur.execute("select * from account where account_id = "+str(record[1]))
        rows = cur.fetchone()
        """ rows = [account_id, balance, acc_status, role] """
        if not rows[2]:
            """ <==> if rows[2] == false"""
            flash('Your account is being LOCKED !')
            return redirect(url_for('show_main_page'))
        else:
            account_id = record[1]
            if rows[3] == 0:
                """ customer """
                role = 0
                return redirect(url_for('show_user_info'))
            else:
                """ bank clerk """
                role = 1
                return redirect(url_for('show_user_info'))


@app.route("/account/find", methods=['GET', 'POST'])
def show_user_info():
    global role, account_id
    cur = conn.cursor()
    cur.execute("select fullname, phone_number from systemUser where account_id = "+str(account_id))
    info = cur.fetchone()
    # info = [fullname, phone_number]

    if role == 1:
        rows = show_account()
        role_name = "Bank clerk"
    elif role == 0:
        rows = show_account(account_id)
        role_name = "Customer"

    account = [{"account_id": r[0], "balance": r[1],
                "account_status": r[2], "role": r[3]} for r in rows]
    return render_template('show_user_info.html', account=account, username=info[0], phone=info[1], role_name=role_name)


@app.route('/register', methods=['GET', 'POST'])
def register():
    global role, created_id
    if role == 0:
        """ this is a customer """
        flash('Customer do not have the right to register another account !!')
        return redirect(url_for('register'))
    elif role == 1:
        """ this is a bank clerk """
        rgt_acc_form = RegisterAccountForm()
        cur = conn.cursor()
        login_name = rgt_acc_form.login_name.data

        if rgt_acc_form.is_submitted():
            cur.execute("select * from loginInfo where login_name = '"+str(login_name)+"\';")
            is_exist = cur.fetchall()

            if len(is_exist) != 0:
                flash('This username already existed !!! ')
            else:
                balance = rgt_acc_form.balance.data
                password_hash = generate_password_hash(rgt_acc_form.register_pass.data)

                if rgt_acc_form.role.data == "Bank Clerk":
                    created_role = 1
                else:
                    created_role = 0

                cur.execute("insert into account(account_id,balance,acc_status,role) values "
                            "(nextval('acc_sequence'),{0},true,{1});".format(balance, created_role))
                conn.commit()

                cur.execute("select account_id from account order by account_id DESC limit 1;")
                created_id = cur.fetchone()[0]
                """ created_id = cur.fetchone --> wrong! """

                cur.execute("insert into loginInfo values"
                            "(\'{0}\',\'{1}\',{2})".format(login_name, password_hash, created_id))
                conn.commit()
                return redirect(url_for('personal_info'))
    return render_template('register.html', title='Add new account', form=rgt_acc_form)


@app.route('/register/personal_info', methods=['GET', 'POST'])
def personal_info():
    psn_in4_form = RegisterPersonalInfoForm()
    if psn_in4_form.is_submitted():
        global created_id
        fullname = psn_in4_form.fullname.data
        address = psn_in4_form.address.data
        phone_number = psn_in4_form.phone_number.data

        cur = conn.cursor()
        cur.execute("insert into systemUser(fullname,address,phone_number,account_id) values"
                    "(\'{0}\',\'{1}\',\'{2}\',{3})".format(fullname, address, phone_number, created_id))
        conn.commit()
        return render_template('successful.html', fullname=fullname, phone_number=phone_number, account_id=created_id)
    return render_template('personal_info.html', form=psn_in4_form)
