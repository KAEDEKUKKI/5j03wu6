\c 5j03wu6;

-- tables
-- Table: user
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name varchar(20)  NOT NULL,
    last_name varchar(50),
    email varchar(255) NOT NULL CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$'),
    passwd varchar(256)  NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT user_ak_1 UNIQUE (email)
);
    
---- Table: device
CREATE TABLE device (
    id SERIAL PRIMARY KEY,
    device_name VARCHAR(100),
    device_type VARCHAR(50),
    registration_date TIMESTAMP DEFAULT NOW()
);

---- Table: group
--CREATE TABLE group (
--    id SERIAL PRIMARY KEY,
--    group_name varchar(50) NOT NULL,
--);

---- Table: user_group
--CREATE TABLE user_group (
--    id SERIAL PRIMARY KEY,
--    group_id int NOT NULL,
--    user_id int NOT NULL,
--);
    
---- Table: user_device
--CREATE TABLE user_device (
--    id SERIAL PRIMARY KEY,
--    user_id int  NOT NULL,
--    device_id int  NOT NULL,
--);

---- Table: group_device
--CREATE TABLE group_device (
--    id SERIAL PRIMARY KEY,
--    group_id int NOT NULL,
--    device_id int NOT NULL,
--);
 
---- foreign keys
---- Reference: user (table: user_device)
--ALTER TABLE user_device ADD CONSTRAINT user
--    FOREIGN KEY (user_id)
--    REFERENCES user (id);
--    
---- Reference: user (table: user_device)
--ALTER TABLE user_device ADD CONSTRAINT device
--    FOREIGN KEY (device_id)
--    REFERENCES device (id);
 