# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, LargeBinary, Numeric, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata

class TblUserPasswdInfo(Base):
    __tablename__ = 'tbl_user_passwd_info'

    user_id = Column(Integer, primary_key=True)
    phone_no = Column(String(13), nullable=False)
    password = Column(String(128), nullable=False)
    salt = Column(Integer, nullable=False)
    crt_dttm = Column(DateTime, nullable=False)
    upd_dttm = Column(DateTime, nullable=False)
    rec_stat = Column(String(1), nullable=False)
    user_stat = Column(Integer, nullable=False)
    err_time = Column(Integer, nullable=False)

class TblRetCodeInfo(Base):
    __tablename__ = 'tbl_ret_code_info'

    ret_code = Column(String(6), primary_key=True)
    ret_code_msg = Column(String(64), nullable=False)
    remark = Column(String(60), nullable=False)
    last_upd_dttm = Column(DateTime, nullable=False)
    record_stat = Column(String(1), nullable=False)

