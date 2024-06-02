from sqlalchemy import Column, Integer, String, Date
from database import Base
 
class Spending(Base):
    __tablename__ = 'spendings'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    date = Column(Date)
    amount = Column(Integer)
    type = Column(String(50))
 
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.isoformat() if self.date else None,
            'amount': self.amount,
            'type': self.type
        }