
import cx_Oracle

# Function to get database connection
def get_connection():
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XEPDB1")
    return cx_Oracle.connect(user="system", password="manager", dsn=dsn)

# Main menu loop
while True:
    print("\n--- ICURD Menu ---")
    print("1. Create Table")
    print("2. insert")
    print("3. Update")
    print("4. Read (Select)")
    print("5. Delete")
    print("6. Exit")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input! Enter a number between 1-6.")
        continue

    match choice:
       # CREATE TABLE
        case 1:
            conn = cur = None
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                    CREATE TABLE stu_info (
                        id NUMBER(10),
                        name VARCHAR2(50),
                        course VARCHAR2(50),
                        CONSTRAINT stu_pk PRIMARY KEY (id, course)
                    )
                """)
                print("Table 'stu_info' Created Successfully!")
            except cx_Oracle.DatabaseError as e:
                print("Error:", e)
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()

       
         # INSERTING TO THE TABLE DATA
        case 2:
            conn = cur = None
            try:
                conn = get_connection()
                cur = conn.cursor()
                id = int(input("Enter ID: "))
                name = input("Enter Name: ")
                course = input("Enter Course: ")

                # Check if ID already exists with a different name
                cur.execute("SELECT name FROM stu_info WHERE id=:1", (id,))
                row = cur.fetchone()
                if row and row[0].lower() != name.lower():
                    print(f"ID {id} is already assigned to {row[0]}, cannot use different name!")
                    continue

                # Check if Name already exists with a different ID
                cur.execute("SELECT id FROM stu_info WHERE LOWER(name)=:1", (name.lower(),))
                row = cur.fetchone()
                if row and row[0] != id:
                    print(f"Name {name} already exists with ID {row[0]}, cannot use different ID!")
                    continue

                # Check duplicate course for same student
                cur.execute("SELECT COUNT(*) FROM stu_info WHERE id=:1 AND course=:2", (id, course))
                count = cur.fetchone()[0]

                if count == 0:
                    cur.execute(
                        "INSERT INTO stu_info (id, name, course) VALUES (:1, :2, :3)",
                        (id, name, course)
                    )
                    conn.commit()
                    print("Record Inserted Successfully!")
                else:
                    print("Duplicate course for this student! Not inserted.")

            except cx_Oracle.DatabaseError as e:
                print("Database Error:", e)
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()

        # UPDATE
        case 3:
            conn = cur = None
            try:
                conn = get_connection()
                cur = conn.cursor()
                id = int(input("Enter ID to update: "))
                old_course = input("Enter old course: ")
                new_course = input("Enter new course: ")

                cur.execute(
                    "UPDATE stu_info SET course=:1 WHERE id=:2 AND course=:3",
                    (new_course, id, old_course)
                )
                conn.commit()

                if cur.rowcount > 0:
                    print("Record Updated Successfully!")
                else:
                    print("No matching record found to update.")

            except cx_Oracle.DatabaseError as e:
                print("Database Error:", e)
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()

        # READ
        case 4:
            conn = cur = None
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("SELECT * FROM stu_info ORDER BY id")
                rows = cur.fetchall()
                print("\nID    NAME               COURSE")
                print("--------------------------------------")
                for r in rows:
                    print(f"{r[0]:<5} {r[1]:<18} {r[2]}")
            except cx_Oracle.DatabaseError as e:
                print("Database Error:", e)
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()

        # DELETE
        case 5:
            conn = cur = None
            try:
                conn = get_connection()
                cur = conn.cursor()
                id = int(input("Enter ID to delete: "))
                course = input("Enter course to delete: ")

                cur.execute(
                    "DELETE FROM stu_info WHERE id=:1 AND course=:2",
                    (id, course)
                )
                conn.commit()

                if cur.rowcount > 0:
                    print("Record Deleted Successfully!")
                else:
                    print("No matching record found to delete.")

            except cx_Oracle.DatabaseError as e:
                print("Database Error:", e)
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()

        # EXIT
        case 6:
            print("Exiting program...")
            break

        # DEFAULT
        case _:
            print("Invalid choice! Please enter a number between 1-6.")
