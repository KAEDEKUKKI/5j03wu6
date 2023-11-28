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

-- Table: device_type
CREATE TABLE type1 (
   id SERIAL PRIMARY KEY,
   type_name VARCHAR(50)
);
    
-- Table: device
CREATE TABLE device (
    id SERIAL PRIMARY KEY,
    device_name VARCHAR(100),
    type_id INT,
    ip_address VARCHAR(15),
    protocol_port INT CHECK (protocol_port BETWEEN 1 AND 65535),
    registration_date TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (type_id) REFERENCES type1 (id) ON DELETE CASCADE
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
   read_p BOOLEAN DEFAULT true,
   write_p BOOLEAN DEFAULT true,
   delete_p BOOLEAN DEFAULT false,
   CONSTRAINT user_group_ak_1 UNIQUE (user_id, group_id),
   FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
   FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE CASCADE
);
    
-- Table: user_device
CREATE TABLE group2 (
   id SERIAL PRIMARY KEY,
   user_id int  NOT NULL,
   device_id int  NOT NULL,
   read_p BOOLEAN DEFAULT true,
   write_p BOOLEAN DEFAULT true,
   delete_p BOOLEAN DEFAULT false,
   CONSTRAINT user_device_ak_1 UNIQUE (user_id, device_id),
   FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
   FOREIGN KEY (device_id) REFERENCES device (id) ON DELETE CASCADE
);

-- Table: group_device
CREATE TABLE group3 (
   id SERIAL PRIMARY KEY,
   group_id int NOT NULL,
   device_id int NOT NULL,
   read_p BOOLEAN DEFAULT true,
   write_p BOOLEAN DEFAULT true,
   delete_p BOOLEAN DEFAULT false,
   CONSTRAINT group_device_ak_1 UNIQUE (group_id, device_id),
   FOREIGN KEY (group_id) REFERENCES groups (id) ON DELETE CASCADE,
   FOREIGN KEY (device_id) REFERENCES device (id) ON DELETE CASCADE
);

INSERT INTO users (id, first_name, last_name, email, passwd) VALUES (1, 'admin', 'san', 'admin@5j03wu6.com', '$2b$12$K1HCRhXEtekW1oCh8psJRu2G01b6czLHiO440UeqGB0pJuY1PkGLi');
INSERT INTO groups (id, group_name) VALUES (1, 'administer');
INSERT INTO group1 (user_id, group_id, read_p, write_p, delete_p) VALUES (1, 1, true, true, true);
INSERT INTO type1 (type_name) VALUES ('camera');