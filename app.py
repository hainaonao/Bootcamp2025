from flask import Flask, render_template
from config import Config
from models import db, Video 
from controllers import init_routes  

app = Flask(__name__)

# Cấu hình ứng dụng từ file config.py
app.config.from_object(Config)

# Khởi tạo SQLAlchemy
db.init_app(app)

# Gọi hàm để đăng ký các route
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)