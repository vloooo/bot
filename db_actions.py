from sqlalchemy import create_engine, ForeignKey, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import text

engine = create_engine('sqlite:///ludmila.db',
                       connect_args={'check_same_thread': False})

Base = declarative_base()
Session = sessionmaker(bind=engine)


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    procedure_id = Column(Integer, ForeignKey('procedure.id'))
    customers = relationship("Customer", back_populates="orders")
    procedures = relationship("Procedure", back_populates="orders")
    datetime = Column(DateTime)


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    herpes = Column(String)
    ledocain = Column(String)
    previously = Column(String)
    orders = relationship('Order', backref='customer', primaryjoin=id == Order.customer_id)
    photos = relationship("Photo", backref="customer")

    def __init__(self, id, first_name, last_name, phone):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone

    def __repr__(self):
        return f"{self.last_name} {self.first_name}, {self.phone}"


class Procedure(Base):
    __tablename__ = 'procedure'

    id = Column(Integer, primary_key=True, autoincrement=True)
    command = Column(String)
    name = Column(String)
    duration = Column(Integer)
    orders = relationship('Order', backref='procedure', primaryjoin=id == Order.procedure_id)

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration


class BlackDates(Base):
    __tablename__ = 'black_dates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)


class Photo(Base):
    """User photos model."""
    __tablename__ = 'customer_pictures'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    path = Column(String)


def get_or_create(session, model, all_fields=None, **kwargs):
    if all_fields:
        id_params = {key: val for key, val in kwargs.items()}
    else:
        id_params = {key: val for key, val in kwargs.items() if 'id' in key}
    instance = session.query(model).filter_by(**id_params).order_by(text('-id')).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


if __name__ == '__main__':
    Base.metadata.create_all(engine)
