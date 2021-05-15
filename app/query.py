from app.db import conn


def show_account(account_id=None):
    cur = conn.cursor()
    sql = "select * from account "
    if account_id:
        sql += "where account_id = " + str(account_id)
    sql += "order by account_id"
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    # conn.close()
    return rows


def show_transaction_history(account_id=None):
    cur = conn.cursor()
    sql = "select t.tran_id, t.tran_date, " \
          "sa.account_id, ssu.fullname, t.money_amt, ra.account_id, rsu.fullname " \
          "from transaction t " \
          "inner join account ra on ra.account_id = t.receiver_id " \
          "inner join systemUser rsu on rsu.account_id = ra.account_id " \
          "inner join account sa on sa.account_id = t.sender_id " \
          "inner join systemUser ssu on ssu.account_id = sa.account_id "
    if account_id:
        sql += "where t.sender_id = " + str(account_id) + " or t.receiver_id = " + str(account_id)
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    return rows
