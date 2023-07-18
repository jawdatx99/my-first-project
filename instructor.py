import sqlite3




class Instructor:
    def __init__(self, id, name):
        self._id = id
        self._name = name

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_courses(self):
        self.fetchCourses()
        return self._courses

    def fetchCourses(self):
        # Fetch courses from database
        from course import Course
        import sqlite3
        con = sqlite3.connect('class-scheduler.db')
        cur = con.cursor()
        cur.execute(
            'SELECT * FROM courses WHERE id IN (SELECT course_id FROM course_instructors WHERE doctor_id = ?)', (self._id,))
        courses = []
        for row in cur:
            courses.append(Course(row[0], row[1], row[2], row[3], row[4]))
        self._courses = courses

    def __str__(self):
        return self._name

    def storeInDatabase(self):
        # Store the instructor in the database
        import sqlite3
        con = sqlite3.connect('class-scheduler.db')
        cur = con.cursor()
        cur.execute('INSERT INTO instructors VALUES (?, ?)',
                    (self._id, self._name))


def AllInstructors():
    # Return a list of all instructors
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM instructors')
    instructors = []
    for row in cur:
        instructors.append(Instructor(row[0], row[1]))
    return instructors


def ReadInstructor(id):
    # Return an instructor object for the given id
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM instructors WHERE id = ?', (id,))
    row = cur.fetchone()
    instructor = Instructor(row[0], row[1])
    return instructor


def CreateInstructor(name):
    # Create a new instructor object and store it in the database
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('INSERT INTO instructors VALUES (?, ?)',
                (None, name))
    con.commit()
    con.close()


def DeleteInstructor(id):
    # Delete an instructor object from the database
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('DELETE FROM instructors WHERE id = ?', (id,))
    con.commit()
    con.close()


def UpdateInstructor(id, name):
    # Update an instructor object in the database
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('UPDATE instructors SET name = ? WHERE id = ?',
                (name, id))
    con.commit()
    con.close()
