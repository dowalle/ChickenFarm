import pandas as pd
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, DECIMAL, VARCHAR, CHAR, INT

from ChickenFarm.src.db.db_fund import Database
from ChickenFarm.src.db.types import Status

Base = declarative_base()


class DepositoryTable(Base):

    __tablename__ = 'tbl_depository'

    name = Column(VARCHAR(255), unique=True, nullable=False)
    code = Column(CHAR(6), primary_key=True)
    filed = Column(VARCHAR(255))
    buying = Column(DECIMAL(10, 2), default=0)
    selling = Column(DECIMAL(10, 2), default=0)
    position = Column(DECIMAL(10, 2), default=0)
    profit = Column(DECIMAL(10, 2), default=0)
    profit_rate = Column(DECIMAL(5, 4), default=0)
    priority = Column(INT, default=0)
    status = Column(VARCHAR(32), default=Status.HOLD, nullable=False)
    update_time = Column(DateTime, onupdate=datetime.now(), default=datetime.now())
    create_time = Column(DateTime, default=datetime.now())
    comment = Column(VARCHAR(255))
    buy_rate = Column(DECIMAL(5, 4))
    sell_rate_info = Column(VARCHAR(255))
    url = Column(VARCHAR(255))

    @staticmethod
    def get_by_code(code):
        return Database().query(DepositoryTable).filter_by(code=code).first()

    @staticmethod
    def get_by_filed(filed):
        # 包含持仓和清仓的基金
        return Database().query(DepositoryTable).filter_by(filed=filed).all()

    @staticmethod
    def get_holding_by_filed(filed):
        # 仅包含持仓中的基金
        return Database().query(DepositoryTable).filter_by(filed=filed) \
                                                .filter_by(status=Status.HOLD) \
                                                .all()

    @staticmethod
    def get_all_holding():
        return Database().query(DepositoryTable).filter_by(status=Status.HOLD).all()

    @staticmethod
    def get_all_holding_code():
        all_holding = DepositoryTable.get_all_holding()
        all_holding_code = [dpt.code for dpt in all_holding]
        return all_holding_code

    @staticmethod
    def get_all():
        return Database().query(DepositoryTable).all()

    def get_attrs(self):
        attrs = []
        for attr in self.__dir__():
            if attr.startswith('_') or attr.startswith('get'):
                continue
            if attr == 'metadata':
                continue
            attrs.append(attr)
        return attrs


def get_fund_dic_from_dpt(code):
    '''
    获取 tbl_depository 表中指定基金的dict，仅可作为展示
    '''
    fund_dpt = DepositoryTable.get_by_code(code)
    if not fund_dpt: return {}

    fund_dpt_dic = {}
    for attr in fund_dpt.get_attrs():
        value = getattr(fund_dpt, attr)
        fund_dpt_dic[attr] = str(value)
    return fund_dpt_dic


def get_filed_pd_from_dpt(filed):
    '''
    获取 tbl_depository 表中指定领域的df，仅可作为展示
    '''
    funds = DepositoryTable.get_holding_by_filed(filed)
    df = pd.DataFrame(columns=['name', 'code', 'buying', 'selling', 
                               'position', 'profit', 'profit_rate', 'priority',])
    for f in funds:
        df = df.append({'name': f.name,
                        'code': f.code,
                        'buying': f.buying,
                        'selling': f.selling,
                        'position': f.position,
                        'profit': f.profit,
                        'profit_rate': f.profit_rate,
                        'priority': f.priority
                        }, ignore_index=True)
    return df.sort_values(by='priority').reset_index(drop=True)


def get_all_pd_from_dpt():
    '''
    获取 tbl_depository 表中所有基金的df，仅可作为展示
    '''
    funds = DepositoryTable.get_all_holding()
    df = pd.DataFrame(columns=['name', 'code', "filed", 'buying', 'selling', 
                               'position', 'profit', 'profit_rate', 'priority',])
    for f in funds:
        df = df.append({'name': f.name,
                        'code': f.code,
                        'filed': f.filed,
                        'buying': f.buying,
                        'selling': f.selling,
                        'position': f.position,
                        'profit': f.profit,
                        'profit_rate': f.profit_rate,
                        'priority': f.priority
                        }, ignore_index=True)
    return df.sort_values(by='filed').reset_index(drop=True)
