import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    all = []
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table (cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs(
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        
        sql = """
            DROP TABLE IF EXISTS dogs

        """
        CURSOR.execute(sql)

    def save(self):

        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))

        self.id = CURSOR.execute ("SELECT last_insert_rowid() FROM dogs").fetchone()[0]

    @classmethod
    def create(cls, name, breed):
        new_dog = Dog(name,breed)
        new_dog.save()
        return new_dog
    
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog
    

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """
        all = CURSOR.execute(sql).fetchall()

        cls.all = [cls.new_from_db(row) for row in all]

        return cls.all

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
        """
        dog = CURSOR.execute(sql, (name,)).fetchone()

        return cls.new_from_db(dog)
    
    @classmethod
    def find_by_id(cls, id):

        sql = """
            SELECT *
            FROM dogs
            WHERE id = ?
        """

        dog = CURSOR.execute(sql, (id, )).fetchone()

        return cls.new_from_db(dog)
    
    @classmethod
    def find_or_create_by(cls, name, breed):

        sql = """
            SELECT *
            FROM dogs
            WHERE name=?
            AND breed=?
        """

        dog_found = CURSOR.execute(sql, (name, breed, )).fetchone()

        if dog_found:
            
            return cls.new_from_db(dog_found)
        else:
            create_dog = cls.create(name, breed)

            return create_dog
    
   
    def update(self, given_name):

        if self.name != given_name:
            
            sql = """
                UPDATE dogs SET name=? 
                WHERE id=?
            """