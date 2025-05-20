from app import db;

class Shift(db.Model):
    __tablename__ = 'shifts'  # Define the table name

    # Define the columns
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    notes = db.Column(db.Text)

    # Foreign keys
    technician_id = db.Column(db.Integer, db.ForeignKey('technicians.id'), nullable=False)
    assigned_equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'), nullable=True)  

    # Define the relationship with the Technician model
    technician = db.relationship('Technician', backref='shifts')
    assigned_equipment = db.relationship('Equipment', backref='shifts')

    def __repr__(self):
        return f"<Shift {self.id} for Technician {self.technician_id} from {self.start_time} to {self.end_time} on {self.date}>"