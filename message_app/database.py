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
    def check(self):
        query = "SELECT * FROM user"
        self.cursor.execute(query)
        print(self.cursor.fetchall())

    def select_user(self, username):
        query = "SELECT username FROM user WHERE username = %s"
        self.cursor.execute(query, (username,))
        user = self.cursor.fetchone()
        if user:
            return True
        else:
            return False

    def select_contacts(self, user_id):
        query = "SELECT id, user1, user2 FROM contacts WHERE user1 = %s OR user2 = %s"
        self.cursor.execute(query, (user_id, user_id))
        contacts = self.cursor.fetchall()
        contacts_info = []

        for contact in contacts:
            temporal_data = {"contact_id": contact[0]}

            if contact[1] == user_id:
                query = "SELECT username FROM user WHERE id = %s"
                self.cursor.execute(query, (contact[2],))
                data = self.cursor.fetchone()

                temporal_data["username"] = data[0]
            else:
                query = "SELECT username FROM user WHERE id = %s"
                self.cursor.execute(query, (contact[1],))
                data = self.cursor.fetchone()

                temporal_data["username"] = data[0]
            
            contacts_info.append(temporal_data)

        if contacts_info:
            return contacts_info
        else:
            return []        


    def select_messages_chat(self, contact_id, user_id):
        query = "SELECT user1, user2 FROM contacts WHERE id = %s"
        self.cursor.execute(query, (contact_id,))
        data = self.cursor.fetchone()

        if not data:
            return []
        if data[0] == user_id:
            user2_id = data[1]
        else:
            user2_id = data[0]
        
        query = "SELECT message FROM messages WHERE (sender = %s AND receiver = %s) OR (sender = %s AND receiver = %s)"
        self.cursor.execute(query, (user_id, user2_id, user2_id, user_id))
        messages = self.cursor.fetchall()

        return messages
    # Check this ^^^^^^^^^^



    def login(self, email, password):
        query = (
            "SELECT id, public_key, username FROM user WHERE email = %s AND user_password = %s"
        )
        self.cursor.execute(query, (email, password))

        data = self.cursor.fetchone()
        if data:
            return data
        else:
            return [None, None, None]

    # INSERT
    def signup(self, email, username, password):
        query = "SELECT id FROM user WHERE email = %s"
        self.cursor.execute(query, (email,))
        if self.cursor.fetchone():
            return [None, None, None]
        
        while True:
            random_id, public_key = self.generate_keys()
            query = "SELECT * FROM user WHERE id = %s OR (public_key = %s AND username = %s)"
            self.cursor.execute(query, (random_id, public_key, username))
            if not self.cursor.fetchone():
                break

        query = "INSERT INTO user (id, email, username, public_key, user_password) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (random_id, email, username, public_key, password))
        self.cnx.commit()

        return random_id, public_key, username

    def insert_contact(self, username, public_key, user_id):
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
        
        return True

    # UPDATE

    # DELETE