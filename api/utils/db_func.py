from datetime import datetime
from . import db


# Database Functions
class DB_Func:
    def save_to_db(self):
        """Saves new data to the database"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deletes data from the database"""
        db.session.delete(self)
        db.session.commit()

    def update_db(self):
        """Updates and commits changes to the database"""
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        """Queries and gets data by Id from a specific table in the database"""
        return cls.query.get_or_404(id)

    @classmethod
    def get_all(cls):
        """Gets all data from a table in the database"""
        return cls.query.all()
