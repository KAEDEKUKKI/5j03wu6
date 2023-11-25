\c 5j03wu6;

-- tables
-- Table: user
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name varchar(20)  NOT NULL,
    last_name varchar(50),
    email varchar(255) NOT NULL CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$'),
    passwd varchar(60)  NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT user_ak_1 UNIQUE (email)
);
    
-- Table: device
CREATE TABLE device (
    id SERIAL PRIMARY KEY,
    device_name VARCHAR(100),
    device_type VARCHAR(50),
    ip_address VARCHAR(15),
    registration_date TIMESTAMP DEFAULT NOW()
);

-- Table: groups
CREATE TABLE groups (
   id SERIAL PRIMARY KEY,
   group_name VARCHAR(50) NOT NULL,
   CONSTRAINT groups_ak_1 UNIQUE (group_name)
);

-- Table: user_group
CREATE TABLE group1 (
   id SERIAL PRIMARY KEY,
   user_id int NOT NULL,
   group_id int NOT NULL,
   CONSTRAINT user_group_ak_1 UNIQUE (user_id, group_id),
   FOREIGN KEY (user_id) REFERENCES users (id),
   FOREIGN KEY (group_id) REFERENCES groups (id)
);
    
-- Table: user_device
CREATE TABLE group2 (
   id SERIAL PRIMARY KEY,
   user_id int  NOT NULL,
   device_id int  NOT NULL,
   CONSTRAINT user_device_ak_1 UNIQUE (user_id, device_id),
   FOREIGN KEY (user_id) REFERENCES users (id),
   FOREIGN KEY (device_id) REFERENCES device (id)
);

-- Table: group_device
CREATE TABLE group3 (
   id SERIAL PRIMARY KEY,
   group_id int NOT NULL,
   device_id int NOT NULL,
   CONSTRAINT group_device_ak_1 UNIQUE (group_id, device_id),
   FOREIGN KEY (group_id) REFERENCES groups (id),
   FOREIGN KEY (device_id) REFERENCES device (id)
);