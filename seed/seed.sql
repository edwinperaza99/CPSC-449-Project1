BEGIN TRANSACTION;
PRAGMA foreign_keys=OFF;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS user_role;
PRAGMA foreign_keys=ON;

CREATE TABLE "role" (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL
);


CREATE TABLE "user" (
    id INTEGER PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);

CREATE TABLE "user_role" (
    id INTEGER PRIMARY KEY,
    user_id int NOT NULL,
    role_id int NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role(id),
    FOREIGN kEY (user_id) REFERENCES user(id)
);

-- role
INSERT INTO role(name) VALUES ("Registrar");
INSERT INTO role(name) VALUES ("Instructor");
INSERT INTO role(name) VALUES ("Student");

-- user
-- INSERT INTO user(username, first_name, last_name, password, role_id) VALUES ("Mr.", "registrar", "registrar1", 1);
-- INSERT INTO user(username, first_name, last_name, password, role_id) VALUES ("Mr.", "instructor1", 2);
-- INSERT INTO user(username, first_name, last_name, password, role_id) VALUES ("Mr.", "instructor1", 2);

COMMIT;