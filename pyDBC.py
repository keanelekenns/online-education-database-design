#CSC 370 A01
#Assignment #3 part 2
#November 23rd
#keanelek_group

import psycopg2
def main():
    #open a connection to the "keanelek_group" database
    con, cur = open_cursor()

    #execute all commands here

    print("The three querys we are looking at are:\n")

    print("One. Figure out best performing students above a given level X that have completed > Y assignments\n")
    #first query
    cur.execute("""SELECT username, average 
                    FROM Students 
                    WHERE level>0 
                    AND numAssignmentsCompleted > 0 
                    ORDER BY average DESC""")
    results = cur.fetchall()
    print("First query results:\n", results)
    print()

    print("Two. When a teacher X logs in, get all unmarked submissions assigned to them\n")
    #second query
    cur.execute("""SELECT submissionId
                    FROM Marks
                    WHERE markedBy='BBird' 
                    AND mark is null""")
    results = cur.fetchall()
    print("Second query results:\n", results)
    print()

    print("Three. When a student logs in, get all worksheets of their level X and language Y available to them\n")
    #third query
    cur.execute("""SELECT templateId, templatepdf
                FROM Templates
                WHERE level=10 
                AND language='english'""")
    results = cur.fetchall()
    print("Third query results:\n", results)
    print()


    #cur.execute("SELECT * FROM students")
    #results = cur.fetchall()
    #print(results)

    #commit changes to DB
    con.commit()

    #close connection and cursor
    close_cursor(con, cur)



#open a cursor to "keanelek_group" as user "tylerjames"
#returns a tuple of (connection object, cursor object)
def open_cursor():
    #open connection
    con = psycopg2.connect(
        host = "studentdb1.csc.uvic.ca",
        database = "keanelek_group",
        user = "keanelekenns",
        password = "studentdb1",
        port = 5432)
    #create DB cursor
    cur = con.cursor()
    #print("remember to close the cursor with"
    #"close_cursor when you are done with it")
    return con, cur

#close cursor to the database
#takes connection object and cursor object as input
def close_cursor(con, cur):
    #close connection and cursor
    cur.close()
    con.close()
    #print("cursor closed")

#function for running a query
def query(queryStatement):
    con, cur = open_cursor()
    cur.execute(queryStatement)
    con.commit()
    print("changes commited\n")
    queryResults = cur.fetchall()
    if queryResults is not None:
        print(queryResults)
    close_cursor(con, cur)

#insert into teachers function
def insert_teachers(username, skypeID, email, language):
    con, cur = open_cursor()
    cur.execute("insert into Teachers (username, skypeID, email, language) values (%s,%s,%s,%s)",
    (username, skypeID, email, language))
    con.commit()
    print("changes commited\n")
    close_cursor(con, cur)

#insert into students function
def insert_students(username, email, language, level, countrylevel):
    con, cur = open_cursor()
    cur.execute("insert into Students (username, email, language, level, countrylevel) values (%s,%s,%s,%s,%s)",
    (username, email, language, level, countrylevel))
    con.commit()
    print("changes commited\n")
    close_cursor(con, cur)

#insert into templates function
def insert_templates(templateid, level, creator, subject, language):
    con, cur = open_cursor()
    cur.execute("insert into Templates (templateid, level, creator, subject, language) values (%s,%s,%s,%s,%s)", 
    (templateid, level, creator, subject, language))
    con.commit()
    print("changes commited\n")
    close_cursor(con, cur)

#insert into submissions function
def insert_submissions(submissionid,templateid,submittedby,timesubmitted):
    con, cur = open_cursor()
    cur.execute("insert into Submissions (submissionid,templateid,submittedby,timesubmitted) values (%s,%s,%s,%s)", 
    (submissionid, templateid, submittedby, timesubmitted))
    con.commit()
    print("changes commited\n")
    close_cursor(con, cur)

#insert into marks function
def insert_marks(submissionId, markedby, mark):
    con, cur = open_cursor()
    cur.execute("insert into Marks (submissionId, markedby, mark) values (%s,%s,%s)", 
    (submissionId, markedby, mark))
    con.commit()
    cur.execute("select submittedby from submissions where submissionId = %s", 
    (submissionId,))
    username = cur.fetchone()
    print(username)
    cur.execute("""UPDATE students SET average = 
    ((average*numAssignmentsCompleted + %s)/(numAssignmentsCompleted + 1)), 
    numAssignmentsCompleted = numAssignmentsCompleted + 1 
    WHERE username = %s""", 
    (mark, username[0]))
    con.commit()
    print("changes commited\n")
    close_cursor(con, cur)
	
#FUNCTION TO CREATE THE DATABASE
def create_database():
    drop_tables()
    create_tables()
    initialise_data()

#function for dropping the tables in the database
def drop_tables():
    con, cur = open_cursor()
    cur.execute("""
        DROP TABLE IF EXISTS marks;
        DROP TABLE IF EXISTS submissions;
        DROP TABLE IF EXISTS teachers;
        DROP TABLE IF EXISTS templates;
        DROP TABLE IF EXISTS students;""")
    con.commit()
    close_cursor(con, cur)

#function for initialising the tables in the database
def create_tables():
    con, cur = open_cursor()
    cur.execute("""
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
        """)
    con.commit()
    close_cursor(con, cur)

def initialise_data():
    con, cur = open_cursor()
    cur.execute("""

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

        INSERT INTO Submissions(submissionid,templateid,submittedby,timesubmitted)
        VALUES (231,3,'KEnns', '2019-11-22 23:17:29-09');
        INSERT INTO Marks(submissionid, markedby, mark)
        VALUES (231,'RLittle', 89.6);
        UPDATE Students SET average = 87.6, numassignmentscompleted = 2 WHERE username='KEnns';
        SELECT username, average, numassignmentscompleted FROM students WHERE username='KEnns';

        INSERT INTO Submissions(submissionid,templateid,submittedby,timesubmitted)
        VALUES (1,4,'JSmith', '2019-06-28 19:10:25-07');

        INSERT INTO Marks(submissionid, markedby)
        VALUES (1,'BBird');
        SELECT submissionId, markedBy, mark FROM marks WHERE submissionID=1;

        SELECT * FROM templates;

        DELETE FROM templates WHERE templateid=5;

        SELECT * FROM templates;

        SELECT * FROM students;
        SELECT * FROM teachers;
        SELECT * FROM templates;
        SELECT * FROM submissions;
        SELECT * FROM marks;

        SELECT username, average
        FROM Students
        WHERE level>0 AND numAssignmentsCompleted > 0
        ORDER BY average DESC;

        SELECT submissionId, submittedpdf
        FROM Marks NATURAL JOIN submissions
        WHERE markedBy='BBird' AND mark is null;

        SELECT templateId, templatepdf
        FROM Templates
        WHERE level=10 AND language='english';
        """)
    con.commit()
    close_cursor(con, cur)
	
	
if __name__ == "__main__":
    main()