from app.db import conn

def show_account(account_id = None):
    cur = conn.cursor()
    sql = "select * from account "
    if account_id:
        sql +=  "where account_id = " + str(account_id)
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    #conn.close()
    return rows