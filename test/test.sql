create table `lock` (
	name varchar(64) primary key
);
insert into `lock` (name) values ('lock1');

create table user (
	id int primary key,
	name varchar(32)
);
insert into user (id, name) values (1, 'user1');
insert into user (id, name) values (2, 'user2');

create table user_setting (
	id int,
	`key` varchar(16),
	value varchar(128),
	primary key (id, `key`)
);
insert into user_setting (id, `key`, value) values (1, 'email', 'user1@test.com');
