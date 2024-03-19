create database milestone4;
use milestone4;

create table Users(
	id int primary key auto_increment,
    username varchar(255) unique not null,
    email varchar(255) unique not null,
    password_hash varchar(255),
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp
);
drop table Users;
create table Accounts(
	id int primary key auto_increment,
    user_id int,
    account_type varchar(255) not null,
    account_number varchar(255) not null,
    balance decimal(10,2) ,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp
);
drop table Accounts;
create table Transactions(
	id int primary key auto_increment,
    from_account_id int,
    to_account_id int,
    amount decimal(10,2) not null,
    type varchar(255),
    description varchar(255),
    created_at timestamp default current_timestamp
);
drop table Transactions;
select * from Users;
select * from Accounts;
select * from Transactions;

ALTER TABLE Users ADD COLUMN role VARCHAR(191) NULL DEFAULT NULL;