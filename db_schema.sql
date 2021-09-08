CREATE TABLE IF NOT EXISTS "projects" (
	"id"	INTEGER NOT NULL,
	"title"	TEXT,
	"success_criteria"	TEXT,
	"status" TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "tasks" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"title"	TEXT,
	"project_id"	INTEGER,
	"status"	TEXT,
	"description"	TEXT,
	"delegate_id"	INTEGER,
	"estimate"	INTEGER,
	"when"	TEXT,
	"priority" INTEGER,
	FOREIGN KEY("project_id") REFERENCES "projects"("id"),
	FOREIGN KEY("delegate_id") REFERENCES "users"("id")
);

INSERT INTO projects (id, title, success_criteria, status) VALUES
(1, 'Get credit', '10000 on bank account', 'Progress'),
(2, 'Buy car', 'Car is in the garage', 'Progress'),
(3, 'Get job', 'First 1000 salary is on bank account ', 'Pending'),
(4, 'Pay debt', 'Credit is paid off', 'Open');

INSERT INTO users (id, name) VALUES
(11, 'Alexander Pushkin'),
(12, 'John Doe'),
(13, 'Jane Doe');

INSERT INTO tasks (id, title, project_id, status, description, delegate_id, estimate, `when`, priority) VALUES
(101, 'Apply for credit', 1, 'Done', 'Find a bank, go to website, apply for credit', null, 10, 'today', 10),
(102, 'Gather docs', 1, 'WIP', 'Passport, etc', 12, 120, 'today', 11),
(103, 'Submit docs', 1, 'Pending', 'Go to the bank and submit docs', null, 120, 'this week', 101),
(104, 'Get approval', 1, 'Pending', 'The bank is to approve. Jane is working in the bank', 13, 10, 'backlog', 1001),
(105, 'Transfer money', 1, 'Pending', 'The bank is to transfer the money', 13, 10, 'backlog', 1020),
(106, 'Find a car to buy', 2, 'Done', 'Find a dealer, go to website, find a car', null, 30, 'today', 10),
(107, 'Pay the credit', 3, 'Backlog', 'After we got a job, pay the credit', 11, 10, 'backlog', 9999);