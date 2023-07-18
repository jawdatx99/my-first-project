import sqlite3

import random as rnd
import prettytable as pt


def geneticAlgorithm():

    population_size = 12
    mutation_rate = 0.02
    tournament_selection_size = 3
    number_of_elite_schedules = 1

    class Data:
        def __init__(self):
            self._rooms = []
            self._meetingTimes = []
            self._instructors = []
            self._courses = []
            self._depts = []

            con = sqlite3.connect('class-scheduler.db')
            cursor = con.cursor()
            for row in cursor.execute('SELECT * FROM `instructors`'):
                self._instructors.append(Instructor(row[0], row[1]))

            for row in cursor.execute('SELECT number,seatingCapacity FROM `rooms`'):
                self._rooms.append(Room(row[0], row[1]))

            for row in cursor.execute('SELECT * FROM `meeting_times`'):
                self._meetingTimes.append(MeetingTime(
                    row[0], row[1] + " " + row[2] + " - " + row[3]))

            for row in cursor.execute('SELECT * FROM `courses`'):
                self._courses.append(
                    Course(id=row[0], number=row[1], name=row[2], maxNumberOfStudents=row[3]))

            for row in cursor.execute('SELECT * FROM `departments`'):
                self._depts.append(Department(id=row[0], name=row[1]))
            cursor.close()

            self._numberOfClasses = 0
            for i in range(0, len(self._depts)):
                self._numberOfClasses += len(self._depts[i].get_courses())

        def get_rooms(self):
            return self._rooms

        def get_meetingTimes(self):
            return self._meetingTimes

        def get_instructors(self):
            return self._instructors

        def get_courses(self):
            return self._courses

        def get_depts(self):
            return self._depts

        def get_numberOfClasses(self):
            return self._numberOfClasses

        def get_depts(self):
            return self._depts

        def get_courses(self):
            return self._courses

        def get_rooms(self):
            return self._rooms

        def get_instructors(self):
            return self._instructors

        def get_meetingTimes(self):
            return self._meetingTimes

        def get_seatingCapacity(self):
            return self._seatingCapacity

    class Schedule:
        def __init__(self):
            self._data = data
            self._classes = []
            self._numberOfConflicts = 0
            self._fitness = -1
            self._classNumb = 0
            self._isFitnessChanged = True

        def get_classes(self):
            self._isFitnessChanged = True
            return self._classes

        def get_numberOfConflicts(self): return self._numberOfConflicts

        def get_fitness(self):
            if self._isFitnessChanged:
                self._fitness = self.calculate_fitness()
                self._isFitnessChanged = False
            return self._fitness

        def initialize(self):
            depts = self._data.get_depts()
            for i in range(0, len(depts)):
                courses = depts[i].get_courses()
                for j in range(0, len(courses)):
                    newClass = Class(self._classNumb, depts[i], courses[j])
                    self._classNumb += 1
                    newClass.set_meetingTime(data.get_meetingTimes(
                    )[rnd.randrange(0, len(data.get_meetingTimes()))])
                    newClass.set_room(
                        data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                    newClass.set_instructor(courses[j].get_instructors(
                    )[rnd.randrange(0, len(courses[j].get_instructors()))])
                    self._classes.append(newClass)
            return self

        def calculate_fitness(self):
            self._numberOfConflicts = 0
            classes = self.get_classes()
            for i in range(0, len(classes)):
                if classes[i].get_room().get_seatingCapacity() < classes[i].get_course().get_seatingCapacity():
                    self._numberOfConflicts += 1
                for j in range(i + 1, len(classes)):
                    if(j >= i):
                        if (classes[i].get_meetingTime() == classes[j].get_meetingTime() and classes[i].get_id() != classes[j].get_id()):
                            if(classes[i].get_room() == classes[j].get_room()):
                                self._numberOfConflicts += 1
                            if(classes[i].get_instructor() == classes[j].get_instructor()):
                                self._numberOfConflicts += 1
            return 1/(self._numberOfConflicts*1.0 + 1)

        def __str__(self):
            returnValue = ""
            for i in range(0, len(self._classes)-1):
                returnValue += str(self._classes[i])+", "
            returnValue += str(self._classes[len(self._classes)-1])
            return returnValue

    class Population:
        def __init__(self, size):
            self._size = size
            self._data = data
            self._schedules = []
            for i in range(0, size):
                self._schedules.append(Schedule().initialize())

        def get_schedules(self):
            return self._schedules

    class GeneticAlgorithm:
        def evolve(self, population): return self._mutate_population(
            self._crossover_population(population))

        def _crossover_population(self, population):
            crossover_population = Population(0)
            for i in range(number_of_elite_schedules):
                crossover_population.get_schedules().append(
                    population.get_schedules()[i])
            i = number_of_elite_schedules
            while i < population_size:
                schedule1 = self._select_tournament_population(
                    population).get_schedules()[0]
                schedule2 = self._select_tournament_population(
                    population).get_schedules()[0]
                crossover_population.get_schedules().append(
                    self._crossover_schedule(schedule1, schedule2))
                i += 1
            return crossover_population

        def _mutate_population(self, population):
            for i in range(number_of_elite_schedules, population_size):
                self._mutate_schedule(population.get_schedules()[i])
            return population

        def _crossover_schedule(self, schedule1: Schedule, schedule2: Schedule):
            crossoverSchedule = Schedule().initialize()
            for i in range(0, len(crossoverSchedule.get_classes())):
                if(rnd.random() > 0.5):
                    crossoverSchedule.get_classes(
                    )[i] = schedule1.get_classes()[i]
                else:
                    crossoverSchedule.get_classes(
                    )[i] = schedule2.get_classes()[i]
            # print(len(schedule1.get_classes()))
            return crossoverSchedule

        def _mutate_schedule(self, mutateSchedule: Schedule):
            schedule = Schedule().initialize()
            for i in range(0, len(mutateSchedule.get_classes())):
                if(mutation_rate > rnd.random()):
                    mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
            return mutateSchedule

        def _select_tournament_population(self, population):
            tournament_population = Population(0)
            i = 0
            while i < tournament_selection_size:
                tournament_population.get_schedules().append(
                    population.get_schedules()[rnd.randrange(0, population_size)])
                i += 1
            tournament_population.get_schedules().sort(
                key=lambda x: x.get_fitness(), reverse=True)
            return tournament_population

    class Room:
        def __init__(self, number, seatingCapacity):
            self._number = number
            self._seatingCapacity = seatingCapacity

        def get_number(self):
            return self._number

        def get_seatingCapacity(self):
            return self._seatingCapacity

    class Course:
        def __init__(self, number, name, instructors, maxNumberOfStudents):
            self._number = number
            self._name = name
            self._instructors = instructors
            self._maxNumberOfStudents = maxNumberOfStudents

        def __init__(self, id, number, name, maxNumberOfStudents):
            self._id = id
            self._number = number
            self._name = name
            self._maxNumberOfStudents = maxNumberOfStudents

        def get_number(self):
            return self._number

        def get_name(self):
            return self._name

        def get_instructors(self):
            self.fetch_instructors()
            return self._instructors

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

        def get_maxNumberOfStudents(self):
            return self._maxNumberOfStudents

        def get_seatingCapacity(self):
            return self._maxNumberOfStudents

        def __str__(self):
            return self._name

    class Department:
        def __init__(self, name, courses):
            self._name = name
            self._courses = courses

        def __init__(self, id, name):
            self._id = id
            self._name = name

        def get_name(self):
            return self._name

        def get_courses(self):
            self.fetch_courses()
            return self._courses

        def fetch_courses(self):
            # Fetch courses from database
            import sqlite3
            con = sqlite3.connect('class-scheduler.db')
            cur = con.cursor()
            cur.execute(
                'SELECT * FROM courses WHERE department_id = ?', (self._id,))
            courses = []
            for row in cur:
                courses.append(Course(id=row[0], number=row[1],
                                      name=row[2], maxNumberOfStudents=row[3]))
            self._courses = courses

    class Instructor:
        def __init__(self, id, name):
            self._id = id
            self._name = name

        def get_id(self):
            return self._id

        def get_name(self):
            return self._name

        def __str__(self):
            return self._name

    class MeetingTime:
        def __init__(self, id, time):
            self._id = id
            self._time = time

        def get_id(self):
            return self._id

        def get_time(self):
            return self._time

    class Class:
        def __init__(self, id, department, course):
            self._id = id
            self._department = department
            self._course = course
            self._instructor = None
            self._meetingTime = None
            self._room = None

        def get_id(self):
            return self._id

        def get_department(self): return self._department
        def get_course(self): return self._course
        def get_instructor(self): return self._instructor
        def get_meetingTime(self): return self._meetingTime
        def get_room(self): return self._room
        def set_instructor(self, instructor): self._instructor = instructor
        def set_meetingTime(self, meetingTime): self._meetingTime = meetingTime
        def set_room(self, room): self._room = room

        def __str__(self):
            return str(self._department.get_name()) + "," + str(self._course.get_number()) + "," + str(self._room.get_number()) + "," + str(self._instructor.get_id()) + "," + str(self._meetingTime.get_id())

    class DisplayManager:
        def print_available_data(self):
            print("> All Available Data")
            
            self.print_course()
            self.print_room()
            self.print_instructor()
            self.print_meetingTimes()

        def print_dept(self):
            depts = data.get_depts()
            availableDeptsTable = pt.PrettyTable(['dept', 'courses'])
            for i in range(0, len(depts)):
                courses = depts.__getitem__(i).get_courses()
                tempStr = "["
                for j in range(0, len(courses) - 1):
                    tempStr += courses[j].__str__() + ", "
                tempStr += courses[len(courses)-1].__str__() + "]"
                availableDeptsTable.add_row(
                    [depts.__getitem__(i).get_name(), tempStr])
            print(availableDeptsTable)

        def print_course(self):
            availableCouresTable = pt.PrettyTable(
                ['id', 'course #', 'max # of students', 'instructors'])
            courses = data.get_courses()
            for i in range(0, len(courses)):
                instructors = courses[i].get_instructors()
                tempStr = "["
                for j in range(0, len(instructors) - 1):
                    tempStr += instructors[j].__str__() + ", "
                tempStr += instructors[len(instructors)-1].__str__() + "]"
                availableCouresTable.add_row(
                    [courses[i].get_number(), courses[i].get_name(), courses[i].get_maxNumberOfStudents(), tempStr])
            print(availableCouresTable)

        def print_instructor(self):
            availableInstructorsTable = pt.PrettyTable(
                ['id', 'instructor'])
            instructors = data.get_instructors()
            for i in range(0, len(instructors)):
                availableInstructorsTable.add_row(
                    [instructors[i].get_id(), instructors[i].get_name()])
            print(availableInstructorsTable)

        def print_generation(self, population):
            generationTable = pt.PrettyTable(
                ['schedule #', 'fitness', '# of conflicts', 'classes [dept,class,room,instructor,meetingTime]'])
            schedules = population.get_schedules()
            for i in range(0, len(schedules)):
                generationTable.add_row([str(i), round(schedules[i].get_fitness(
                ), 3), schedules[i].get_numberOfConflicts(), schedules[i].get_classes()])

        def print_room(self):
            availableRoomsTable = pt.PrettyTable(
                ['room #', 'seating capacity'])
            rooms = data.get_rooms()
            for i in range(0, len(rooms)):
                availableRoomsTable.add_row(
                    [rooms[i].get_number(), rooms[i].get_seatingCapacity()])
            print(availableRoomsTable)

        def print_meetingTimes(self):
            availableMeetingTimesTable = pt.PrettyTable(
                ['id', 'time'])
            meetingTimes = data.get_meetingTimes()
            for i in range(0, len(meetingTimes)):
                availableMeetingTimesTable.add_row(
                    [meetingTimes[i].get_id(), meetingTimes[i].get_time()])
            print(availableMeetingTimesTable)

        def print_schedule(self, schedule: Schedule):
            classes = schedule.get_classes()
            table = pt.PrettyTable(['Class #', 'Dept', 'Course (number, max # of students)',
                                    'Room (Capacity)', 'Instructor', 'Meeting Time'])
            for i in range(0, len(classes)):
                table.add_row([
                    str(i),
                    classes[i].get_department().get_name(),
                    classes[i].get_course().get_name() + " (" + str(classes[i].get_course().get_number(
                    )) + ", " + str(classes[i].get_course().get_maxNumberOfStudents())+")",
                    classes[i].get_room().get_number(),
                    classes[i].get_instructor().get_name(),
                    classes[i].get_meetingTime().get_time()
                ])
            print(table)

    data = Data()
    displayManager = DisplayManager()
    displayManager.print_available_data()
    generationNumber = 0
    print("\n> Generation #" + str(generationNumber))
    population = Population(population_size)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    displayManager.print_generation(population)
    displayManager.print_schedule(population.get_schedules()[0])
    geneticAlgorithm = GeneticAlgorithm()
    while (population.get_schedules()[0].get_fitness() != 1.0):
        generationNumber += 1
        print("\n> Generation #" + str(generationNumber))
        population = geneticAlgorithm.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        displayManager.print_generation(population)
        displayManager.print_schedule(population.get_schedules()[0])
        print("\n> Fitness score: " +
              str(population.get_schedules()[0].get_fitness()))
        if(generationNumber > 300 ):
            return False
    print("\n\n")
    return (population.get_schedules()[0])
