import sqlite3


def init_db():
    conn = sqlite3.connect("carsharing.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY, 
                 name TEXT UNIQUE, 
                 password TEXT,
                 phoneNumber TEXT,
                 driverLicense TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS cars (
                 id INTEGER PRIMARY KEY, 
                 vin TEXT UNIQUE, 
                 location TEXT, 
                 available INTEGER)""")

    c.execute("INSERT OR IGNORE INTO users (name, password, phoneNumber, driverLicense) VALUES ('user1', 'pass1', '0722222222', 'DL111')")
    c.execute("INSERT OR IGNORE INTO cars (vin, location, available) VALUES ('VIN123', 'Bucuresti', 1)")
    c.execute("INSERT OR IGNORE INTO cars (vin, location, available) VALUES ('VIN456', 'Cluj', 1)")
    c.execute("INSERT OR IGNORE INTO cars (vin, location, available) VALUES ('VIN789', 'Timisoara', 1)")
    c.execute("INSERT OR IGNORE INTO cars (vin, location, available) VALUES ('VIN101', 'Iasi', 1)")
    c.execute("INSERT OR IGNORE INTO cars (vin, location, available) VALUES ('VIN112', 'Brasov', 1)")
    c.execute("INSERT OR IGNORE INTO cars (vin, location, available) VALUES ('VIN131', 'Constanta', 1)")
    c.execute("INSERT OR IGNORE INTO cars (vin, location, available) VALUES ('VIN141', 'Iasi', 1)")
    c.execute("INSERT OR IGNORE INTO cars (vin, location, available) VALUES ('VIN151', 'Timisoara', 1)")
    c.execute("INSERT OR IGNORE INTO cars (vin, location, available) VALUES ('VIN161', 'Cluj', 1)")
    c.execute("INSERT OR IGNORE INTO cars (vin, location, available) VALUES ('VIN171', 'Bucuresti', 1)")
    c.execute("INSERT OR IGNORE INTO cars (vin, location, available) VALUES ('VIN181', 'Brasov', 1)")
    c.execute("INSERT OR IGNORE INTO cars (vin, location, available) VALUES ('VIN134', 'Constanta', 1)")
    c.execute("INSERT OR IGNORE INTO cars (vin, location, available) VALUES ('VIN144', 'Iasi', 1)")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Baza de date a fost inițializată.")
