import psycopg2
from werkzeug.security import generate_password_hash
""" install: pip3.6 install psycopg2-binary """
""" used to connect python and postgreSQL """

conn = psycopg2.connect(host="localhost", port="5432", database="ITJPBank",
                        user="postgres", password="lboEDG82")
        

cur = conn.cursor()

# "account" table
cur.execute("create table if not exists account(account_id serial primary key, "
            "balance int,acc_status boolean,role int);")
conn.commit()
""" commit (v) = confirm to execute """

# "systemUser" table
cur.execute("create table if not exists systemUser(su_id SERIAL primary key,fullname varchar(30),"
            "account_id int,address varchar(30),phone_number varchar(15),"
            "constraint su_acc foreign key (account_id) references account(account_id));")
conn.commit()

# "transaction" table
cur.execute("create table if not exists transaction(tran_id serial primary key,"
            "money_amt int,tran_date date,sender_id int,receiver_id int,"
            "constraint tran_send foreign key (sender_id) references account(account_id),"
            "constraint tran_receive foreign key (receiver_id) references account(account_id));")
conn.commit()

# "card_owning" table
cur.execute("create table if not exists card_owning(account_id int,card_id int,"
            "constraint card_acc foreign key (account_id) references account(account_id));")
conn.commit()

# "loginInfo" table
cur.execute("create table if not exists loginInfo(login_name varchar(30) primary key,"
            "password_hash varchar(200),account_id int,"
            "constraint acc_login foreign key (account_id) references account(account_id));")
conn.commit()


""" *****   INIT FOR MANAGER's "login_name & password"   ***** """
cur.execute("delete from loginInfo where account_id = 10000;")
conn.commit()

origin_pass = "123456"
hash_pass = generate_password_hash(origin_pass)
login_name = "manager"

cur.execute("insert into loginInfo(login_name,password_hash,account_id)"
            "values(\'{0}\',\'{1}\',10000);".format(login_name, hash_pass))
conn.commit()
