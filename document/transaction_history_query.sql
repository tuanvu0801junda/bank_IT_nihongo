select t.tran_id, t.money_amt, t.tran_date,
sa.account_id, ssu.fullname,
ra.account_id, rsu.fullname
from transaction t
inner join account ra on ra.account_id = t.receiver_id
inner join systemUser rsu on rsu.account_id = ra.account_id
--inner join systemUser rsu using(account_id)
inner join account sa on sa.account_id = t.sender_id
inner join systemUser ssu on ssu.account_id = sa.account_id
where t.sender_id = 10003 or t.receiver_id = 10003

select * from transaction

select * from account

select * from loginInfo
delete from loginInfo where account_id = 10005
