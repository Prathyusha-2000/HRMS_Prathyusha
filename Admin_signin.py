import mysql.connector
from mysql.connector import Error

class AdminAuthentication:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def authenticate_admin(self, username, password):
        try:
            # Establish a MySQL connection
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )

            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)
                # Query to fetch admin data based on username
                query = "SELECT * FROM admin_table WHERE username = %s"
                cursor.execute(query, (username,))
                admin = cursor.fetchone()

                if admin and admin['password'] == password:
                    return True
                else:
                    return False

        except Error as e:
            print("Error: ", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        return False

class AdminRegistration:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def register_admin(self, username, password):
        try:
            # Establish a MySQL connection
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )

            if connection.is_connected():
                cursor = connection.cursor()
                # Query to insert a new admin user
                query = "INSERT INTO admin_table (username, password) VALUES (%s, %s)"
                cursor.execute(query, (username, password))
                connection.commit()
                print("New admin user registered successfully!")

        except Error as e:
            print("Error: ", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def admin_sign_in_or_register():
    db_host = 'localhost'
    db_name = 'hrms_database'
    db_user = 'root'
    db_password = 'PRA#23kgrw9'

    choice = input("Enter '1' to sign in or '2' to register: ")

    if choice == '1':
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        auth = AdminAuthentication(db_host, db_name, db_user, db_password)
        if auth.authenticate_admin(username, password):
            print("Login successful. Welcome, Admin!")
        else:
            print("Invalid username or password. Please try again.")
    elif choice == '2':
        username = input("Enter a new username: ")
        password = input("Enter a new password: ")

        registration = AdminRegistration(db_host, db_name, db_user, db_password)
        registration.register_admin(username, password)
    else:
        print("Invalid choice. Please enter '1' to sign in or '2' to register.")

if __name__ == "__main__":
    admin_sign_in_or_register()
