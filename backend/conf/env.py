# ================================================= #
# ************** mysql数据库 配置  ************** #
# ================================================= #
# 数据库类型 MYSQL/SQLSERVER/SQLITE3
DATABASE_TYPE = "MYSQL"
# 数据库地址
DATABASE_HOST = "101.42.19.26"
# 数据库端口
DATABASE_PORT = 3306
# 数据库用户名
DATABASE_USER = "root"
# 数据库密码
DATABASE_PASSWORD = "Qwe134134@"
# 数据库名
DATABASE_NAME = "ddi_admin"

# ================================================= #
# ************** redis配置，无redis 可不进行配置  ************** #
# ================================================= #
REDIS_PASSWORD = '123456'
REDIS_HOST = '101.42.19.26'
REDIS_URL = f'redis://:{REDIS_PASSWORD or ""}@{REDIS_HOST}:6379'
# ================================================= #
# ************** 其他 配置  ************** #
# ================================================= #
DEBUG = True  # 线上环境请设置为False
ALLOWED_HOSTS = ["*"]
# LOGIN_NO_CAPTCHA_AUTH = True
LOGIN_NO_CAPTCHA_AUTH = False  # 登录接口 /api/token/ 是否需要验证码认证，用于测试，正式环境建议取消
ENABLE_LOGIN_ANALYSIS_LOG = True  # 启动登录详细概略获取(通过调用api获取ip详细地址)

# 是否开启演示环境，开启后增 删 改功能失效
DEMO = False
