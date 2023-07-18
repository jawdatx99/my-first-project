from flask import Flask, redirect, render_template, request
from numpy import require
from course import AllCourses, CreateCourse, CreateCourseInstructor, DeleteCourse, ReadCourse
from department import AllDepartments, CreateDepartment, DeleteDepartment
from geneticAlgorithm import geneticAlgorithm

from instructor import AllInstructors, CreateInstructor, DeleteInstructor, ReadInstructor
from meetingTimes import AllMeetingTimes, CreateMeetingTime, DeleteMeetingTime
from room import AllRooms, CreateRoom, DeleteRoom


# Implement flask to show the result in web form
if __name__ == '__main__':
    app = Flask(__name__)

    # Doctors
    @app.route('/')
    def doctorsIndex():
        doctors = AllInstructors()
        return render_template('doctors.html', doctors=doctors)

    @app.route('/doctors/<int:id>/delete', methods=['POST'])
    def deleteDoctor(id):
        DeleteInstructor(id)
        return redirect('/')

    @app.route('/doctors/<int:id>/edit', methods=['GET'])
    def editDoctor(id):
        doctor = ReadInstructor(id)
        return render_template('editDoctor.html', doctor=doctor)

    @app.route('/doctors/create', methods=['GET'])
    def createDoctor():
        return render_template('add-doctor.html')

    @app.route('/doctors', methods=['POST'])
    def storeDoctor():
        name = request.form['name']
        CreateInstructor(name)
        return redirect('/')

    # Rooms
    @app.route('/rooms')
    def roomsIndex():
        rooms = AllRooms()
        return render_template('rooms.html', rooms=rooms)

    @app.route('/rooms/create')
    def createRoom():
        return render_template('add-room.html')

    @app.route('/rooms/<int:id>/edit', methods=['GET'])
    def editRoom(id):
        return render_template('edit-room.html')

    @app.route('/rooms/<int:id>/delete', methods=['POST'])
    def deleteRoom(id):
        DeleteRoom(id)
        return redirect('/rooms')

    @app.route('/rooms', methods=['POST'])
    def storeRoom():
        seatingCapacity = request.form['seatingCapacity']
        number = request.form['number']
        CreateRoom(number, seatingCapacity)
        return redirect('/rooms')

    # Meeting Times
    @app.route('/meeting-times')
    def meetingTimesIndex():
        meetingTimes = AllMeetingTimes()
        return render_template('meeting_times.html', meetingTimes=meetingTimes)

    @app.route('/meeting-times/create')
    def createMeetingTime():
        return render_template('add-meeting_times.html')

    @app.route('/meeting-times', methods=['POST'])
    def storeMeetingTime():
        day = request.form['day']
        startTime = request.form['startTime']
        endTime = request.form['endTime']
        CreateMeetingTime(day, startTime, endTime)
        return redirect('/meeting-times')

    @app.route('/meeting-times/<int:id>/delete', methods=['POST'])
    def deleteMeetingTime(id):
        DeleteMeetingTime(id)
        return redirect('/meeting-times')

    # Departments
    @app.route('/departments')
    def departmentsIndex():
        departments = AllDepartments()
        return render_template('departments.html', departments=departments)

    @app.route('/departments/create')
    def createDepartment():
        return render_template('add-department.html')

    @app.route('/departments/<int:id>/delete', methods=['POST'])
    def deleteDepartment(id):
        DeleteDepartment(id)
        return redirect('/departments')

    @app.route('/departments', methods=['POST'])
    def storeDepartment():
        CreateDepartment(request.form['name'])
        return redirect('/departments')

    # Courses
    @app.route('/courses')
    def coursesIndex():
        courses = AllCourses()
        return render_template('courses.html', courses=courses)

    @app.route('/courses/create')
    def createCourse():
        doctors = AllInstructors()
        departments = AllDepartments()
        return render_template('add-course.html', doctors=doctors, departments=departments)

    @app.route('/courses', methods=['POST'])
    def storeCourse():
        number = request.form['number']
        name = request.form['name']
        maxNumberOfStudents = request.form['max_number_of_students']
        department_id = request.form['department_id']
        # create a course and retrieve the id
        CreateCourse(number, name, maxNumberOfStudents, department_id)
        createdCourse = ReadCourse(number)
        for entry in request.form.getlist('doctor_id[]'):
            CreateCourseInstructor(createdCourse.get_id(), entry)
        return redirect('/courses')

    @app.route('/courses/<int:id>/delete', methods=['POST'])
    def deleteCourse(id):
        DeleteCourse(id)
        return redirect('/courses')
    
    # Schedule
    @app.route('/schedule')
    def scheduleIndex():    
        schedule = geneticAlgorithm()
        if schedule == False:
            return render_template('error-page.html', schedule=False)
        return render_template('schedule.html', data=schedule)
        

    @app.route('/style.css')
    def style():
        return app.send_static_file('style.css')

    app.run(debug=True)
