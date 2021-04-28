drop table if exists account cascade;
create table account(
account_id serial primary key,
balance int,
acc_status boolean,
role int
);


drop table if exists systemUser cascade;
create table systemUser(
su_id SERIAL primary key,
fullname varchar(30),
account_id int,
address varchar(30),
phone_number varchar(15),
constraint su_acc foreign key (account_id) references account(account_id)
);


drop table if exists transaction cascade;
create table transaction(
tran_id serial primary key,
money_amt int,
tran_date date,
sender_id int,
receiver_id int,
constraint tran_send foreign key (sender_id) references account(account_id),
constraint tran_receive foreign key (receiver_id) references account(account_id)
);


drop table if exists card_owning cascade;
create table card_owning(
account_id int,
card_id int,
constraint card_acc foreign key (account_id) references account(account_id)
);


drop table if exists loginInfo cascade;
create table loginInfo(
login_name varchar(30) primary key,
password_hash varchar(200),
account_id int,
constraint acc_login foreign key (account_id) references account(account_id)
);