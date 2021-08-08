from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, DECIMAL, VARCHAR, CHAR, INT

from apollo.src.db_model.database import Database
from apollo.src.prof_model.fund_types import Status


Base = declarative_base()


class DepositoryTable(Base):

    __tablename__ = 'tbl_depository'

    name = Column(VARCHAR(255), unique=True, nullable=False)
    code = Column(CHAR(6), primary_key=True)
    filed = Column(VARCHAR(255))
    buying = Column(DECIMAL(10, 2), nullable=False)
    selling = Column(DECIMAL(10, 2), default=0)
    position = Column(DECIMAL(10, 2), nullable=False)
    profit = Column(DECIMAL(5, 2), default=0)
    profit_rate = Column(DECIMAL(5, 4), default=0)
    priority = Column(INT, default=0)
    status = Column(VARCHAR(32), default=Status.HOLD, nullable=False)
    update_time = Column(DateTime, onupdate=datetime.now, default=datetime.now)
    create_time = Column(DateTime, default=datetime.now)
    comment = Column(VARCHAR(255))

    @staticmethod
    def get_by_code(code):
        return Database().query(DepositoryTable).filter_by(code=code).one()

    def get_attrs(self):
        attrs = []
        for attr in self.__dir__():
            if attr.startswith('_') or attr.startswith('get'):
                continue
            if attr == 'metadata':
                continue
            attrs.append(attr)
        return attrs






