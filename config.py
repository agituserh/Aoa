SECRET_KEY="bhdigfgu:jhddu;jldf" #session-cookic 加密字符越长越安全，但是解密时间会变长

HOSTNAME = '127.0.0.1'
PORT = 3306
DATABASE = 'aoa_db'
USERNAME = 'root'
PASSWORD = ''

# 构造数据库连接 URI（以 MySQL 为例）
DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

# SQLAlchemy 配置项
SQLALCHEMY_DATABASE_URI = DB_URI

# 邮箱配置示例（QQ邮箱）
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_SSL = True #加密
MAIL_USE_TLS = False
MAIL_USERNAME = "@qq.com"
MAIL_PASSWORD = ""
MAIL_DEFAULT_SENDER = "@qq.com"


REDIS_URL = "redis://localhost:6379/0"