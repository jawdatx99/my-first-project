class Department:
    def __init__(self, name, courses):
        self._name = name
        self._courses = courses

    def __init__(self, name) -> None:
        self._name = name

    def __init__(self, id, name) -> None:
        self._id = id
        self._name = name

    def get_name(self):
        return self._name

    def set_id(self, id):
        self._id = id

    def get_id(self):
        return self._id

    def fetch_courses(self):
        from course import Course
        # Fetch courses from database
        import sqlite3
        con = sqlite3.connect('class-scheduler.db')
        cur = con.cursor()
        cur.execute(
            'SELECT * FROM courses WHERE department_id = ?', (self._id,))
        courses = []
        for row in cur:
            courses.append(Course(id=row[0], number=row[1],
                                  name=row[2], maxNumberOfStudents=row[3], department_id=row[4]))
        self._courses = courses

    def get_courses(self):
        self.fetch_courses()
        return self._courses


def AllDepartments():
    # Return a list of all departments
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM departments')
    departments = []
    for row in cur:
        departments.append(Department(id=row[0], name=row[1]))
    return departments


def ReadDepartment(id):
    # Return a department object for the given id
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM departments WHERE id = ?', (id,))
    row = cur.fetchone()
    department = Department(id=row[0], name=row[1])
    return department


def CreateDepartment(name):
    # Create a new department object and store it in the database
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('INSERT INTO departments VALUES (?, ?)',
                (None, name))
    con.commit()
    con.close()


def DeleteDepartment(id):
    # Delete a department object from the database
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('DELETE FROM departments WHERE id = ?', (id,))
    con.commit()
    con.close()
    