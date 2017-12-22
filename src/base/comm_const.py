# -*- coding:utf-8 -*-
#from base.const import *
import const
import datetime
import math

const.RECORD_AVA   = '1'
const.RECORD_UNAVA = '0'

###########################微办公公众号#####################################################

const.GET_ACCESS_TOKEN_URL = 'https://168.1.6.140:9016/auth/token.action?'
const.MODIFY_USER_GROUP_URL = 'https://168.1.6.140:9016/group/move.action?access_token='
const.CREATE_MENU_URL       = 'https://168.1.6.140:9016/menu/new.action?access_token='
const.QUERY_GROUP_URL       = 'https://168.1.6.140:9016/group/query.action?access_token='
const.CREATE_MATERIAL_INFO_URL = 'https://168.1.6.140:9016/mass/material.action?access_token='
const.PUSH_MATERIAL_INFO_URL = 'https://168.1.6.140:9016/mass/masspush.action?access_token='

const.PUBLIC_PLAT_RET_ACCESS_TOKEN_ERROR   = 40001
const.PUBLIC_PLAT_RET_ACCESS_TOKEN_INVALID = 40014
const.PUBLIC_PLAT_RET_SUCCESS              = 0

const.PUBLIC_PLAT_CLIENT_ID = '993811722a236be827420d1756d9e4f4'
const.PUBLIC_PLAT_CLIENT_SECRET = 'f8f59feb07cf05874b152850937c19c1'

const.PUBLIC_PLAT_MSG_TYPE_TEXT  = 'text'
const.PUBLIC_PLAT_MSG_TYPE_EVENT = 'event'

const.PUBLIC_PLAT_METERIAL_TYPE_NEWS = 'mpnews'

const.IT_DEP_GROUP = 431                  
const.OTHER_DEP_GROUP = 432

const.REDIS_ACCESS_TOKEN = 'ACCESS_TOKEN'

const.RMB_DEPOSIT_SUM_PARA_TYPE_ID = 0
const.RMB_DEPOSIT_CORP_PARA_TYPE_ID = 2
const.RMB_DEPOSIT_RETAIL_PARA_TYPE_ID = 4

############################################################################################

#message
const.VER_CODE_UNCHECKED = '0'
const.VER_CODE_CHECKED   = '1'
#const.MSG_TIMEOUT = 5
const.VER_CODE_TPYE_REGISTER = '0'   #验证码类型为注册
const.VER_CODE_TPYE_PHONE_NO = '1'   #验证码类型为修改手机号
const.VER_CODE_TPYE_PASSWD = '2'     #验证码类型为修改密码
const.MESSAGE_URL = 'http://api.ict-china.com/do/smsApi!mt.shtml'   #短信平台URL
const.CPID = 4200    #短信平台用户id
const.USERPASS = 'aac6571795143b8a447808f4c29eede8'   #短信平台密码的md5值
const.PORT = 581782   #短信平台扩展码
const.LOGO = "【享充】"   #短信平台签名
const.ALERT = "【请勿向任何人提供您收到的短信验证码】"   #短信平台警告语
const.CPMID = '88888888888'      # 短信平台ID，用常量


const.CODE_EXPIRE_TIME = 5  #设置超时时间 分           
const.SESSION_EXPIRE_SEC = 7 * 24 * 3600

const.LOGIN_OPT_LOGOUT   = 0
const.LOGIN_OPT_LOGIN    = 1

const.USER_LOCK_STAT = 1  #用户锁定状态
const.PASSWD_MAX_TIME = 5 #用户密码尝试次数最大值

'''
 返回码0开头的为成功，commit
 其他的为失败，rollback
'''
const.RET_SUCCESS      = '00000'
#const.RET_CHARGING_FINISH      = '00001'  #充电结束 !!!!
const.RET_STARTING_CHARGING    = '00001'  #开始充电准备中
const.RET_STOPING_CHARGING     = '00002'  #结束用电准备中
const.RET_APP_UNCONNECT        = '00003'  #APP还未进行过扫码充电


const.RET_SYS_ERROR    = '20001'
const.RET_ARG_ERROR    = '20002'
const.RET_DB_ERROR     = '20003'
const.RET_DB_NOTFOUND  = '20007' #数据库查无记录
const.RET_MEMDB_ERROR  = '20004' #redis error
const.RET_MEMDB_KEY_ERROR  = '20006' #redis key error, cannot find key-value
const.RET_USER_LOCK_ERROR    = '20007'  #用户被锁定
const.RET_MESSAGE_ERROR = '20008'  #短信平台发生错误



const.RET_MSG_VER_CODE_ERROR    = '30001'
const.RET_MSG_VER_CODE_EXPIRE   = '30002'
const.RET_MSG_VER_CODE_UNAPPLY  = '30003'
const.RET_PHONE_NO_EXIST        = '30004' #phone_no already exist
const.RET_PASSWD_ERROR          = '30005' #passwd error
const.RET_PHONE_NO_NOT_EXIST    = '30006' #phone_no not exist
const.RET_USER_ID_NOT_EXIST     = '30007' #userid not exist
const.RET_USER_ID_NOT_LOGIN     = '30008' #userid not login
const.RET_SESSION_EXPIRE        = '30012' #session过期，需重新登录
const.RET_LOGIN_OTHER_TERM      = '30009' #has been logged in to other terminal
const.RET_CODE_IN_FROCE         = '30010' #code still in force
const.RET_CHARGER_ID_NOT_EXIST  = '30011'
const.RET_MSG_VER_CODE_CHECKED_ERROR = '30013'  #验证码已被使用
const.RET_MSG_VER_CODE_TYPE_ERROR = '30014'   #验证码类型错误




const.DEFAULT_TIMEDATE_STR    = '2000-01-01 0:0:0'
const.DEFALUT_TIMEDATE  = datetime.datetime.strptime(const.DEFAULT_TIMEDATE_STR,'%Y-%m-%d %H:%M:%S')

const.SESSION_KEY  = 'iamthekey,guessme'



#const.REDIS_session_id_correct = 1        
const.REDIS_SESSION_ID_CORRECT  = 1

'''
 for tornado server
'''
const.RET_COMMAND_IP_ERROR     = '30101'  #控制充电桩IP错误，不在白名单内
const.RET_CHARGER_IP_ERROR     = '30102'  #充电桩IP错误，不在白名单内
const.RET_CHARGER_ID_EXIST     = '30103'  #充电桩ID已经连接tornado

'''
for command
'''
const.RET_COMMAND_NOT_EXECUTE  = '30201'   #还存在未执行的指令
const.RET_COMMAND_SRC_ERROR    = '30202'   #指令源错误
const.RET_COMMAND_ERROR        = '30203'   #指令执行异常 
const.COMMAND_CHARGING         = '2'      #充电指令
const.COMMAND_STOP_CHARGING    = '3'      #停止充电指令
const.COMMAND_AUTHORIZATION    = '1'      #授权指令
const.COMMAND_UPDATE           = '4'      #更新程序指令
const.NOT_AUTHORIZATION        = '0'
const.AUTHORIZATION            = '1'

'''
for charger
'''
const.CHARGER_STAT_INITIAL          = '00'     #初始状态
const.CHARGER_STAT_READY            = '01'     #空闲状态，可以充电, 未连接
const.CHARGER_STAT_CONNECT_CAR      = '02'     #已连接汽车
const.CHARGER_STAT_CHARGING         = '03'     #充电中
const.CHARGER_STAT_PROG_UPDATING    = '04'     #充电桩程序更新中
const.CHARGER_STAT_UNREACHABLE      = '10'     #充电桩网络不可达
const.CHARGER_STAT_BROKEN           = '20'     #充电桩充电模块等已损坏,网络模块正常
const.CHARGER_STAT_STEAL            = '21'     #充电桩盗电
const.CHARGER_STAT_NOT_RET          = '30'     #枪未插入锁槽
const.MAX_ERR_TIMES                 = 5


const.RET_IN_CHARGE            = '30301'  #正在充电中
const.RET_NOT_CONNECT          = '30302'  #充电桩未连接
const.RET_IN_FAULT             = '30303'  #充电桩故障
const.RET_CONNECT              = '30304'  #充电桩已连接
const.RET_CHARGER_AUTH         = '30309'  #充电桩已授权
const.RET_CHARGER_UNAUTH       = '30310'  #充电桩未授权
const.RET_BAL_IS_NONE          = '30305'  #余额为0
const.RET_FALUT_IN_CHARGE      = '30306'  #充电异常
const.RET_STST_ERROR           = '30307'  #充电桩状态异常
const.RET_CHARGE_ERROR         = '30308'  #充电桩偷电异常



'''
 <todo> 放入到配置表中
'''
const.MAX_DELTA_IN_CHARGE      = 0.5    #充电时电量差的最大值
const.MAX_DELTA_NOT_IN_CHARGE  = 0.2    #非充电时电量差的最大值

'''
for account
'''
const.RET_ACCOUNT_ID_NOT_EXIST = '30401' #帐户表中没有相应user_id记录
const.RET_AREA_INFO_NOT_EXIST  = '30402' #充电桩地理信息没有记录

'''
for management
 <todo> 放入到配置表中 , 这是配置信息，不是常量
'''
const.CHARGER_INFO_DIR         = '/dvlp/ichrg_repos/data/import_data'  #充电桩导入路径



const.HTML_APIS = 'html_apis'    #html api目录

'''
for pay
'''
#const.API_KEY = 'sk_test_KuXvHOOu1uzDTGSiPKGiTKSS' #secret key,测试模式下
const.API_KEY = 'sk_live_1uDOC0bjrTG4ufHuv14mT08G' #live模式下
const.APP_ID = 'app_5SeLu1OuD4CSLGOa' #应用ID
const.PRIVATE_KEY = 'rsa_private_key.pem'
const.CURRENCY = 'cny' #三位 ISO 货币代码，目前仅支持人民币  cny
const.SUBJECT = 'xiang_charge' #商品的标题
const.BODY = 'user_charge' #商品的描述信息

'''
for map
'''
const.MAP_URL = 'http://api.map.baidu.com/geocoder/v2/'  #百度地图服务地址
const.AK = 'fra9wSaquk0av9RdQ6ZotBEQtRvMIOGN'
const.EARTH_RADIUS = 6378137
const.RAD = math.pi/180.0
const.TYPEAC = '0'     #交流类型
const.TPYEDC = '1'     #直流类型

'''
for mine
'''
const.UPLOAD_PATH = '/dvlp/ichrg_repos/web/avatar/'
const.DEFALUT_IMAGE = 'default.jpg'
const.PAY_LIMIT = 10  #充电查询每页显示条数
const.CHARGE_LIMIT = 10   #充值查询每页显示条数
const.IMAGE_PATH = '/dvlp/ichrg_repos/web/image'    #默认的图片路径
const.HTML_PATH = '/dvlp/ichrg_repos/web/html'


'''
管理台
'''
const.SUPER_ADMIN_ROLE_TYPE = '0' #超级管理员角色类型






