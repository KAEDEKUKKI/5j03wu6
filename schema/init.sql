-- tables
-- Table: user
CREATE TABLE user (
    id int  NOT NULL IDENTITY(1, 1),
    name varchar(20)  NOT NULL,
    passwd varchar(100)  NOT NULL CHECK (LENGTH(passwd) >= 6),
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP  NULL,
    CONSTRAINT user_ak_1 UNIQUE (name, passwd),
    CONSTRAINT user_pk PRIMARY KEY  (id)
);
    
-- Table: device
CREATE TABLE device (
    id int  NOT NULL IDENTITY(1, 1),
    keys char(32)  NOT NULL,
    name varchar(20)  NOT NULL,
    CONSTRAINT device_ak_1 PRIMARY KEY  (keys),
    CONSTRAINT device_pk PRIMARY KEY  (id)
);
    
-- Table: user_device
CREATE TABLE user_device (
    id int  NOT NULL IDENTITY(1, 1),
    user_id int  NOT NULL,
    device_id int  NOT NULL,
    CONSTRAINT user_device_pk PRIMARY KEY  (id)
);
    
-- foreign keys
-- Reference: user (table: user_device)
ALTER TABLE user_device ADD CONSTRAINT user
    FOREIGN KEY (user_id)
    REFERENCES user (id);
    
-- Reference: user (table: user_device)
ALTER TABLE user_device ADD CONSTRAINT device
    FOREIGN KEY (device_id)
    REFERENCES device (id);
 