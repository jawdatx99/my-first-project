import sqlite3


class Room:
    def __init__(self, id, number, seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity
        self._id = id

    def get_number(self):
        return self._number

    def get_id(self):
        return self._id

    def get_seatingCapacity(self):
        return self._seatingCapacity


def AllRooms():
    # Return a list of all rooms
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM rooms')
    rooms = []
    for row in cur:
        rooms.append(Room(row[0], row[1], row[2]))
    return rooms


def ReadRoom(number):
    # Return an room object for the given number
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM rooms WHERE number = ?', (number,))
    row = cur.fetchone()
    room = Room(row[0], row[1])
    return room


def CreateRoom(number, seatingCapacity):
    # Create a new room object and store it in the database
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('INSERT INTO rooms (id,number,seatingCapacity) VALUES (?, ?, ?)',
                (None, number, seatingCapacity))
    con.commit()
    con.close()


def DeleteRoom(number):
    # Delete an room object from the database
    import sqlite3
    con = sqlite3.connect('class-scheduler.db')
    cur = con.cursor()
    cur.execute('DELETE FROM rooms WHERE id = ?', (number,))
    con.commit()
    con.close()

