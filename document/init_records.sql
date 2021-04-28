drop sequence if exists acc_sequence;
create sequence acc_sequence start 10000

/* INSERT "account" TABLE */
insert into account(account_id,balance,acc_status,role) values (nextval('acc_sequence'),10000000,true,1);

/* INSERT "systemUser" TABLE */
insert into systemUser(fullname,account_id,address,phone_number) values ('Bank Manager',10000,'23 Tran Hung Dao','092.232.2332');

/* INSERT "transaction" TABLE */
/*
insert into transaction(money_amt,tran_date,sender_id,receiver_id) values (15000000,'2021-5-9',32910,95412);
insert into transaction(money_amt,tran_date,sender_id,receiver_id) values (1500000,'2021-6-9',32910,35410);
*/

select * from account
select * from systemUser
select * from transaction
select * from loginInfo
select * from card_owning

delete from account 
delete from systemUser
delete from transaction
delete from loginInfo
delete from card_owning

select account_id from account order by account_id DESC limit 1