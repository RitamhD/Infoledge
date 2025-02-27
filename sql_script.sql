create database Infoledge;
use Infoledge;
show tables;

CREATE TABLE credentials(
user_id int AUTO_INCREMENT PRIMARY KEY NOT NULL,
user_name varchar(20),
user_email varchar(100) UNIQUE NOT NULL,
user_password varchar(20) NOT NULL
);

desc credentials;
select * from credentials;
SET SQL_SAFE_UPDATES = 0;
delete from credentials;
SET SQL_SAFE_UPDATES = 1;

drop table credentials;
