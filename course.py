from instructor import Instructor


class Course:
    def __init__(self, number, name, instructors, maxNumberOfStudents):
        self._number = number
        self._name = name
        self._instructors = instructors
        self._maxNumberOfStudents = maxNumberOfStudents

    def __init__(self, id, number, name, maxNumberOfStudents, department_id) -> None:
        self._id = id
        self._number = number
        self._name = name
        self._maxNumberOfStudents = maxNumberOfStudents
        self._department_id = department_id

    def get_number(self):
        return self._number

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def get_instructors(self):
        self.fetch_instructors()
        return self._instructors

    def get_maxNumberOfStudents(self):
        return self._maxNumberOfStudents

    def fetch_instructors(self):
        # Fetch instructors from database
        import sqlite3
        con = sqlite3.connect('class-scheduler.db')
        cur = con.cursor()
        cur.execute(
            'SELECT * FROM instructors WHERE id IN (SELECT doctor_id FROM course_instructors WHERE course_id = ?)', (self._id,))
        instructors = []
        for row in cur:
            instructors.append(Instructor(row[0], row[1]))
        self._instructors = instructors

    def __str__(self):
        return self._name


def AllCourses():
    # Return a list of all courses
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM courses')
    courses = []
    for row in cur:
        courses.append(Course(id=row[0], number=row[1],
                              name=row[2], maxNumberOfStudents=row[3], department_id=row[4]))
    cur.close()
    return courses


def ReadCourse(number):
    # Return a course object for the given number
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM courses WHERE number = ?', (number,))
    row = cur.fetchone()
    cur.close()
    course = Course(id=row[0], number=row[1],
                    name=row[2], maxNumberOfStudents=row[3],department_id=row[4])
    return course


def CreateCourse(number, name, maxNumberOfStudents, department_id):
    # Create a new course object, store it in the database and return it

    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    print(cur.execute('INSERT INTO courses (id,number,name,max_number_of_students,department_id) VALUES (?, ?, ?, ?, ?)',
                      (None, number, name, maxNumberOfStudents, department_id)))
    con.commit()
    con.close()


def CreateCourseInstructor(course_id, instructor_id):
    # Create a new course object, store it in the database and return it
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('INSERT INTO course_instructors (id,course_id,doctor_id) VALUES (?,?, ?)',
                (None, course_id, instructor_id))
    con.commit()
    con.close()

def DeleteCourse(id):
    # Delete a course object from the database
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('DELETE FROM courses WHERE id = ?', (id,))
    con.commit()
    con.close()