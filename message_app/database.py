import random
import string
import mysql.connector


class Database:
    def __init__(self):
        self.cnx = mysql.connector.connect(
            host="127.0.0.1",
            port=3303,
            user="root",
            password="123",
            database="messageDatabase",
        )

        self.cursor = self.cnx.cursor()

    def generate_keys(self):
        random_id = "".join(random.choice(string.ascii_letters) for _ in range(20))
        public_key = "".join(random.choice(string.ascii_uppercase) for _ in range(3))

        return random_id, public_key

    # SELECT
    def select_user(self, username):
        query = "SELECT username FROM user WHERE username = %s"
        self.cursor.execute(query, (username,))
        user = self.cursor.fetchone()
        if user:
            return True
        else:
            return False

    def login(self, username, password):
        query = (
            "SELECT id, public_key FROM user WHERE username = %s AND user_password = %s"
        )
        self.cursor.execute(query, (username, password))

        data = self.cursor.fetchone()
        if data:
            return data
        else:
            return [None, None]

    # INSERT
    def signup(self, username, password):
        while True:
            random_id, public_key = self.generate_keys()
            query = "SELECT * FROM user WHERE id = %s OR (public_key = %s AND username = %s)"
            self.cursor.execute(query, (random_id, public_key, username))
            if not self.cursor.fetchone():
                break

        query = "INSERT INTO user (id, username, public_key, user_password) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (random_id, username, public_key, password))
        self.cnx.commit()

        return random_id, public_key

    def add_contact(self, username, public_key, user_id):
        # Ceck if the contact exists
        query = "SELECT id FROM contacts WHERE user1 = %s AND user2 = %s"
        self.cursor.execute(query, (username, public_key))
        if self.cursor.fetchone():
            return False

        # Check if the user exists
        query = "SELECT id FROM user WHERE username = %s AND public_key = %s"
        self.cursor.execute(query, (username, public_key))
        id = self.cursor.fetchone()
        if not id:
            return False

        while True:
            random_id = self.generate_keys()[0]
            query = "SELECT * FROM contacts WHERE id = %s"
            self.cursor.execute(query, (random_id,))
            if not self.cursor.fetchone():
                break

        query = "INSERT INTO contacts (id, user1, user2) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (random_id, user_id, id[0]))
        self.cnx.commit()

    # UPDATE

    # DELETE
