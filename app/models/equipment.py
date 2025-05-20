from app import db

class Equipment(db.Model):
    __tablename__ = 'equipments'  # Define the table name

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False)  
    type = db.Column(db.String(50), nullable=False)  
    location = db.Column(db.String(100), nullable=True)  
    status = db.Column(db.String(30), default="operational")  
    last_maintenance = db.Column(db.Date, nullable=True)  

    assisigned_to = db.Column(db.Integer, db.ForeignKey('technicians.id'), nullable=True)  # link to technicians table

    def __repr__(self):
        return f"<Equipment {self.name} - {self.status}>"