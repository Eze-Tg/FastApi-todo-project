DROP TABLE IF EXISTS users;

CREATE TABLE users (
	id SERIAL,
	email varchar(200)DEFAULT NULL,
	username varchar(45)DEFAULT NULL,
	first_name varchar(45)DEFAULT NULL,
	last_name varchar(45)DEFAULT NULL,
	hashed_password varchar(200)DEFAULT NULL,
	is_active boolean DEFAULT NULL,
	role varchar(45)DEFAULT NULL,
	PRIMARY KEY(id)
);


DROP TABLE IF EXISTS todos;

CREATE TABLE Todos (
	id SERIAL,
	title varchar(200)DEFAULT NULL,
	description varchar(200)DEFAULT NULL,
	prioty integer DEFAULT NULL,
	completed boolean DEFAULT NULL,
	owner_id integer DEFAULT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY (owner_id) REFERENCES users(id)
);