class Config:
    SECRET_KEY = 'mysecretkey123'  # Chuỗi bí mật để bảo mật
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123TIEN@localhost/eduspark'
    SQLALCHEMY_TRACK_MODIFICATIONS = False