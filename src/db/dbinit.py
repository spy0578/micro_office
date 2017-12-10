# -*- coding:utf-8 -*-
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import *
import time
from dborm.dborm import *
from etc.config import *


'''
init db
'''
def init_db(engine) :
    #create all tables
    Base.metadata.create_all(engine)
def drop_db(engine) :
    #drop all tables
    Base.metadata.drop_all(engine)


print configs[config_type].SQLALCHEMY_URI

#engine = create_engine(configs[config_type].SQLALCHEMY_URI,
#                       pool_size=int(configs[config_type].SQLALCHEMY_POOL_SIZE),
#                       echo=False)

engine = create_engine(configs[config_type].SQLALCHEMY_URI,
                       echo=True)


init_db(engine)
'''
 create session factory
 DBSession is Class!!!
'''
DBSession = sessionmaker(bind=engine)

