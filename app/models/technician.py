from app import db;

class Technician(db.Model):
    __tablename__ = 'technicians' # defined the table name

    # Define the columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=True)
    skills = db.Column(db.String(200), nullable=True)
    available_from = db.Column(db.Time)
    available_to = db.Column(db.Time)
    
    def __repr__(self):
        return f"<Technician {self.name}>"