from flask import render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from app import app
""" import app == import "app" in __init__.py """
from app.db import conn
from app.query import show_account, show_transaction_history
from app.form import RegisterAccountForm, RegisterPersonalInfoForm, SendMoneyForm
from app.form import ClerkLockAccountForm, ClerkUnLockAccountForm

role = account_id = created_id = -1
receiver_id = money_amt = acc_lock = acc_unlock = -1
fullname = ""


@app.route('/')
def show_main_page():
    return render_template('index.html', logStatus=1)

  
@app.route('/login', methods=['GET', 'POST'])
def login():
    global account_id, role
    username = request.form.get('username')
    password = request.form.get('login_pass')
    cur = conn.cursor()
    cur.execute("select password_hash, account_id from loginInfo where login_name = "+"\'"+username+"\';")
    record = cur.fetchone()
    """ record = [password_hash, acc_login]"""

    if not check_password_hash(record[0], password):
        return render_template('warning.html', message="Invalid user name or password!")
    else:
        cur.execute("select * from account where account_id = "+str(record[1]))
        rows = cur.fetchone()
        """ rows = [account_id, balance, acc_status, role] """
        if not rows[2]:
            """ <==> if rows[2] == false"""
            return render_template('warning.html', message="Your account is being LOCKED !")
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


@app.route("/account", methods=['GET', 'POST'])
def show_user_info():
    global rows
    cur = conn.cursor()
    cur.execute("select fullname, phone_number from systemUser where account_id = "+str(account_id))
    info = cur.fetchone()
    # info = [fullname, phone_number]

    if role == 1 or role == 0:
        cur.execute("select balance from account where account_id = " + str(account_id))
        balance = cur.fetchone()[0]
        if role == 1:
            rows = show_account()
            all_account = [{"account_id": r[0], "balance": r[1],
                "account_status": r[2], "role": r[3]} for r in rows]
            # role_name = "Bank clerk"
            return render_template('manager.html', logStatus=0, card_holder=info[0],
                               card_number=account_id, balance=balance, account=all_account)
        elif role == 0:
            rows = show_account(account_id)
            # role_name = "Customer" (ctm)
            ctm_account = [{"account_id": r[0], "balance": r[1],
                        "account_status": r[2], "role": r[3]} for r in rows]
            return render_template('index.html', logStatus=0, card_holder=info[0],
                               card_number=account_id, balance=balance, account=ctm_account)
    return render_template('index.html', logStatus=1)


@app.route('/register', methods=['GET', 'POST'])
def register():
    global created_id
    if role == 0:
        """ this is a customer """
        return render_template('warning.html',
                               message="Customer do not have the right to register another account !!")
    elif role == 1:
        """ this is a bank clerk """
        rgt_acc_form = RegisterAccountForm()
        cur = conn.cursor()
        login_name = request.form.get('login_name')

        if rgt_acc_form.is_submitted():
            cur.execute("select * from loginInfo where login_name = '"+str(login_name)+"\';")
            is_exist = cur.fetchall()

            if len(is_exist) != 0:
                return render_template('warning.html',
                                       message="This username already existed !!!")
            else:
                balance = request.form.get('balance')
                password_hash = generate_password_hash(request.form.get('register_pass'))

                if request.form.get('role') == "Bank clerk":
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
              

@app.route('/register_render')
def register_render():
    return render_template('register.html')


@app.route('/register/input_personal_info', methods=['GET', 'POST'])
def personal_info():
    psn_in4_form = RegisterPersonalInfoForm()
    if psn_in4_form.is_submitted():
        global fullname
        fullname = psn_in4_form.fullname.data
        address = psn_in4_form.address.data
        phone_number = psn_in4_form.phone_number.data

        cur = conn.cursor()
        cur.execute("insert into systemUser(fullname,address,phone_number,account_id) values"
                    "(\'{0}\',\'{1}\',\'{2}\',{3})".format(fullname, address, phone_number, created_id))
        conn.commit()
        return render_template('successful.html', fullname=fullname, phone_number=phone_number, account_id=created_id)
    return render_template('personal_info.html', form=psn_in4_form)


@app.route('/send_money', methods=['GET', 'POST'])
def send_money():
    send_money_form = SendMoneyForm()
    if send_money_form.is_submitted():
        global receiver_id, money_amt
        money_amt = send_money_form.money_amt.data
        receiver_id = send_money_form.receiver_account.data
        message = send_money_form.message.data

        cur = conn.cursor()
        cur.execute("select balance from account natural join systemUser where account_id = "+str(account_id))
        balance_check = cur.fetchone()[0]

        if balance_check < money_amt:
            return render_template('warning.html',
                                   message="Money amount which will be sent is more than BALANCE!")
        else:
            cur.execute("select fullname from systemUser where account_id = "+str(receiver_id))
            receiver_name = cur.fetchone()[0]
            if len(receiver_name) == 0:
                return render_template('warning.html',
                                       message="No suitable receiver existed!")
            else:
                cur.execute("select fullname from systemUser where account_id = "+str(account_id))
                sender_name = cur.fetchone()[0]
                return render_template('send_confirm.html', receiver_id=receiver_id, receiver_name=receiver_name,
                                       money_amt=money_amt, fullname=sender_name, sender_id=account_id, message=message, role=role)
    return render_template('send_money.html', form=send_money_form, role=role)


@app.route('/send_money/confirm', methods=['GET', 'POST'])
def confirm_send_money():
    cur = conn.cursor()
    cur.execute("update account set balance = balance + "+str(money_amt)
                + " where account_id = "+str(receiver_id))
    conn.commit()

    cur.execute("update account set balance = balance - "+str(money_amt)
                + " where account_id = "+str(account_id))
    conn.commit()

    moment = datetime.datetime.now()
    cur.execute("insert into transaction(money_amt,sender_id,receiver_id,tran_date)"
                "values(" + str(money_amt) + "," + str(account_id) + "," + str(receiver_id) +
                ",\'"+moment.strftime('%Y-%m-%d %X')+"\')")
    conn.commit()
    return render_template('sent_successful.html', role=role)


@app.route('/show_trans_history', methods=['GET', 'POST'])
def show_trans_history():
    cur = conn.cursor()
    if role == 1:
        """ bank clerk """
        all_rows = show_transaction_history()
        all_trans = [{"tran_id": x[0], "tran_date": x[1], "sender_id": x[2], "sender_name": x[3],
                      "money_amt": x[4], "receiver_id": x[5], "receiver_name": x[6]} for x in all_rows]
        return render_template('show_transaction.html', transaction=all_trans, role=1,
                               account_id=account_id, cus_name="")

    elif role == 0:
        """ customer """
        cus_rows = show_transaction_history(account_id)
        cus_trans = [{"tran_id": x[0], "tran_date": x[1], "sender_id": x[2], "sender_name": x[3],
                      "money_amt": x[4], "receiver_id": x[5], "receiver_name": x[6]} for x in cus_rows]
        cur.execute("select fullname from systemUser where account_id = " + str(account_id))
        cus_name = cur.fetchone()[0]
        return render_template('show_transaction.html', transaction=cus_trans, account_id=account_id,
                               cus_name=cus_name, role=0)


@app.route('/lock_account', methods=['POST', 'GET'])
def lock_account():
    cur = conn.cursor()
    global acc_lock
    if role == 1:
        """bank clerk """
        return render_template('acc_lock_by_clerk.html')

    elif role == 0:
        """ customer """
        cur.execute("select fullname from systemUser where account_id = " + str(account_id))
        ctm_name = cur.fetchone()[0]
        return render_template('acc_lock_by_ctm.html', account_id=account_id, ctm_name=ctm_name)


@app.route('/lock_confirm', methods=['POST', 'GET'])
def lock_confirm():
    cur = conn.cursor()
    if role == 1:
        """ bank clerk """
        acc_lock = request.form.get('acc_lock')
        cur.execute("update account set acc_status = false where account_id = "+str(acc_lock))
        return redirect(url_for('show_user_info'))

    elif role == 0:
        """ customer """
        cur.execute("update account set acc_status = false where account_id = "+str(account_id))
        return redirect(url_for('logout'))


@app.route('/unlock_account', methods=['POST', 'GET'])
def unlock_account():
    global acc_unlock
    if role == 1:
        """ bank clerk """
        return render_template('unlock_account.html')
    elif role == 0:
        return render_template('warning.html', message="Customer CANNOT UNLOCK. Ask Bank Clerk for helps!")


@app.route('/unlock_confirm', methods=['POST', 'GET'])
def unlock_confirm():
    if role == 1:
        cur = conn.cursor()
        acc_unlock = request.form.get('acc_unlock')
        cur.execute("update account set acc_status = true where account_id = "+str(acc_unlock))
        return redirect(url_for('show_user_info'))


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    global role, account_id, created_id, receiver_id, money_amt
    global money_amt, acc_unlock, acc_lock, fullname
    
    role = account_id = created_id = -1
    receiver_id = money_amt = acc_lock = acc_unlock = -1
    fullname = ""
    return redirect(url_for('show_main_page'))
