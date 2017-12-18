# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, LargeBinary, Numeric, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata



class TblParaStatInfo(Base):
    __tablename__ = 'tbl_para_stat_info'

    para_id         = Column(Integer, primary_key=True)
    para_type_id    = Column(Integer, nullable=False)
    para_id_name    = Column(String(20), nullable=False)
    para_type_name  = Column(String(20), nullable=False)
    figure          = Column(Numeric(8, 2), nullable=False)
    figure_dttm     = Column(DateTime, nullable=False)
    remark          = Column(String(60), nullable=False)
    record_stat     = Column(String(1), nullable=False)




class TblOlLogInfo(Base):
    __tablename__ = 'tbl_ol_log_info'

    serial_num    = Column(Integer, primary_key=True)
    user_id       = Column(Integer, nullable=False)
    service       = Column(String(128), nullable=False)
    ret_code      = Column(String(10), nullable=False)
    remark        = Column(String(60), nullable=False)
    last_upd_dttm = Column(DateTime, nullable=False)
    record_stat   = Column(String(1), nullable=False)


class TblUserBasicInfo(Base):
    __tablename__ = 'tbl_user_basic_info'

    user_id       = Column(Integer, primary_key=True)
    phone_no      = Column(String(13), nullable=False)
    notes_user_id = Column(String(20), nullable=False)
    notes_id      = Column(String(10), nullable=False)
    user_stat     = Column(String(1), nullable=False)
    crt_dttm      = Column(DateTime, nullable=False)
    last_upd_dttm = Column(DateTime, nullable=False)    
    record_stat   = Column(String(1), nullable=False)

class TblRetCodeInfo(Base):
    __tablename__ = 'tbl_ret_code_info'

    ret_code      = Column(String(6), primary_key=True)
    ret_code_msg  = Column(String(64), nullable=False)
    remark        = Column(String(60), nullable=False)
    last_upd_dttm = Column(DateTime, nullable=False)
    record_stat   = Column(String(1), nullable=False)

