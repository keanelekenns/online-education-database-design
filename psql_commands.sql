-- \echo Drop all tables if they exist '\n'

DROP TABLE IF EXISTS marks;
DROP TABLE IF EXISTS submissions;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS templates;
DROP TABLE IF EXISTS students;

-- \echo '\n'Perform initial creation of tables'\n'

CREATE TABLE Teachers(
username VARCHAR(50) NOT NULL PRIMARY KEY,
skypeId VARCHAR(50) NOT NULL,
email VARCHAR(50) NOT NULL,
language VARCHAR(50) NOT NULL);

CREATE TABLE Students(
username VARCHAR(50)  NOT NULL PRIMARY KEY,
email varchar(50) NOT NULL,
language varchar(50) NOT NULL,
level smallint NOT NULL,
countryLevel smallint NOT NULL,
average real NOT NULL DEFAULT 0,
numAssignmentsCompleted smallint NOT NULL DEFAULT 0);

CREATE TABLE Templates(
templateId integer NOT NULL PRIMARY KEY,
level smallint NOT NULL,
creator varchar(50) NOT NULL,
subject varchar(50) NOT NULL,
language varchar(50) NOT NULL,
templatepdf bytea);

CREATE TABLE Submissions(
submissionId integer NOT NULL Primary key,
templateId integer NOT NULL REFERENCES Templates(templateId),
submittedBy varchar(50) NOT NULL REFERENCES Students(username),
timeSubmitted TIMESTAMPTZ NOT NULL,
submittedpdf bytea);

CREATE TABLE Marks(
submissionId integer NOT NULL PRIMARY KEY REFERENCES Submissions(submissionId),
markedBy varchar(50) NOT NULL REFERENCES Teachers(username),
mark real CHECK (mark <= 100 AND mark >= 0),
markedpdf bytea);


-- \echo '\n'Insert and update data in tables'\n'

INSERT INTO Teachers (username, skypeid, email, language)
VALUES ('BBird', 'bird75', 'bbird@uvic.ca', 'english'),
('MZastre', 'MrZ25', 'mzastre@uvic.ca', 'german'),
('IThomo', '123', 'thomo@uvic.ca', 'greek'),
('VKing', 'king85', 'vking@uvic.ca', 'english'),
('RLittle', 'littlerich320', 'rlittle@uvic.ca', 'english');

INSERT INTO Students (username, email, language, level, countrylevel)
VALUES ('TJames', 'tylerjames@uvic.ca', 'english',8,9),
('NComeau', 'natcomeau@uvic.ca', 'spanish',13,13),
('KEnns', 'keanelekenns@uvic.ca', 'german',11,0),
('BBoy', 'bobbyboy@uvic.ca', 'english',15,-1),
('JSmith', 'johnsmith@uvic.ca', 'english',12,12);

UPDATE students SET countrylevel=5 WHERE countrylevel <0;

INSERT INTO Templates(templateid, level, creator, subject, language)
VALUES (1,10,'Mr. Jenkins', 'algebra', 'english'),
(2,11,'Dr. Goluskin', 'geometry', 'spanish'),
(3,14,'Dr. Jing Huang', 'calculus', 'german'),
(4, 19,'Dr. Bob', 'combinatorics', 'english'),
(5, 20, 'Tom Thomson', 'complex', 'english');

INSERT INTO Submissions(submissionid,templateid,submittedby,timesubmitted)
VALUES (123, 1,'KEnns', '2016-06-22 19:10:25-07'),
(111,2,'NComeau', '2017-06-22 19:10:25-07'),
(9939,1,'TJames', '2018-06-22 19:10:25-07'),
(235,4,'BBoy', '2019-06-22 19:10:25-07');


-- \echo '\n'Whenever we add a mark, we need to update the students average.
-- \echo We will have external logic to get the students current average and calculate what the new one should be.'\n'
-- \echo First, add the marked assignment to our database
-- \echo Next, get the current average and number of assignments completed of the student matching the submission
-- \echo Then, update the average and number of assignments'\n'

INSERT INTO Marks(submissionId, markedby, mark)
VALUES (123,'BBird', 85.6);
UPDATE Students SET average = 85.6, numassignmentscompleted = 1 WHERE username='KEnns';
SELECT username, average, numassignmentscompleted FROM students WHERE username='KEnns';

INSERT INTO Marks(submissionId, markedby, mark)
VALUES (111,'IThomo', 99.99);
UPDATE Students SET average = 99.99, numassignmentscompleted = 1 WHERE username='NComeau';
SELECT username, average, numassignmentscompleted FROM students WHERE username='NComeau';

INSERT INTO Marks(submissionId, markedby, mark)
VALUES (9939,'VKing', 92);
UPDATE Students SET average = 92, numassignmentscompleted = 1 WHERE username='TJames';
SELECT username, average, numassignmentscompleted FROM students WHERE username='TJames';


INSERT INTO Marks(submissionId, markedby, mark)
VALUES (235,'RLittle',49.5);
UPDATE Students SET average = 49.5, numassignmentscompleted = 1 WHERE username='BBoy';
SELECT username, average, numassignmentscompleted FROM students WHERE username='BBoy';


-- \echo '\n'Add another submission with a mark and update average/numAssignmentsCompleted'\n'

INSERT INTO Submissions(submissionid,templateid,submittedby,timesubmitted)
VALUES (231,3,'KEnns', '2019-11-22 23:17:29-09');
INSERT INTO Marks(submissionid, markedby, mark)
VALUES (231,'RLittle', 89.6);
UPDATE Students SET average = 87.6, numassignmentscompleted = 2 WHERE username='KEnns';
SELECT username, average, numassignmentscompleted FROM students WHERE username='KEnns';

-- \echo '\n'Add submission and assign teacher, but no mark is inserted yet'\n'

INSERT INTO Submissions(submissionid,templateid,submittedby,timesubmitted)
VALUES (1,4,'JSmith', '2019-06-28 19:10:25-07');

INSERT INTO Marks(submissionid, markedby)
VALUES (1,'BBird');
SELECT submissionId, markedBy, mark FROM marks WHERE submissionID=1;

-- \echo '\n'Remove an unused template'\n'

-- \echo '\n'TEMPLATES BEFORE:'\n'

SELECT * FROM templates;

DELETE FROM templates WHERE templateid=5;

-- \echo '\n'TEMPLATES AFTER:'\n'

SELECT * FROM templates;

-- \echo '\n'Get information from all tables'\n'

SELECT * FROM students;
SELECT * FROM teachers;
SELECT * FROM templates;
SELECT * FROM submissions;
SELECT * FROM marks;

-- \echo '\n'Run sample queries'\n'

-- \echo '\n'Figure out best performing students above a given level X that have completed > Y assignments'\n'

SELECT username, average
FROM Students
WHERE level>0 AND numAssignmentsCompleted > 0
ORDER BY average DESC;

-- \echo '\n'When a teacher X logs in, get all unmarked submissions assigned to them'\n'

SELECT submissionId, submittedpdf
FROM Marks NATURAL JOIN submissions
WHERE markedBy='BBird' AND mark is null;

-- \echo '\n'When a student logs in, get all worksheets of their level X and language Y available to them'\n'

SELECT templateId, templatepdf
FROM Templates
WHERE level=10 AND language='english';




