class MeetingTime:
    def __init__(self, id, time):
        self._id = id
        self._time = time

    def get_id(self):
        return self._id

    def get_time(self):
        return self._time

    def set_day(self, day):
        self._day = day

    def set_range(self, range):
        self._range = range

    def get_range(self):
        return self._range

    def get_day(self):
        return self._day

    def __str__(self):
        return self._time


def AllMeetingTimes():
    # Return a list of all meeting times
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM meeting_times')
    meetingTimes = []
    for row in cur:
        displayTime = row[1] + " " + row[2] + " - " + row[3]
        mT = MeetingTime(row[0], displayTime)
        mT.set_day(row[1])
        mT.set_range(row[2] + " - " + row[3])
        meetingTimes.append(mT)
    return meetingTimes


def CreateMeetingTime(day, startTime, endTime):
    # Create a new meeting time object and store it in the database
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('INSERT INTO meeting_times VALUES (?, ?, ?, ?)',
                (None, day, startTime, endTime))
    con.commit()
    con.close()

def DeleteMeetingTime(id):
    # Delete an meeting time object from the database
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('DELETE FROM meeting_times WHERE id = ?', (id,))
    con.commit()
    con.close()