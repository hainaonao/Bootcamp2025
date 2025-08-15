from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Khởi tạo SQLAlchemy
db = SQLAlchemy()

# Mô hình User
class User(db.Model):
    __tablename__ = 'users'  # Tên bảng trong cơ sở dữ liệu

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100))
    role = db.Column(db.Enum('teacher', 'student', 'parent', 'admin'), nullable=False)
    profile = db.relationship('UserProfile', back_populates='user', uselist=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Mô hình Lesson
class Lesson(db.Model):
    __tablename__ = 'lessons'  # Tên bảng trong cơ sở dữ liệu

    lesson_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    grade_level = db.Column(db.Integer)
    subject = db.Column(db.String(50))

    def __repr__(self):
        return f'<Lesson {self.title}>'

# Mô hình Video
class Video(db.Model):
    __tablename__ = 'videos'  # Tên bảng trong cơ sở dữ liệu

    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    principle = db.Column(db.Text)
    view = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    thumbnail = db.Column(db.String(255), default=None)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))  # Khóa ngoại tới bảng 'users'
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.lesson_id'))  # Khóa ngoại tới bảng 'lessons'
    url_video = db.Column(db.String(255))

    # Mối quan hệ với bảng Lesson và User
    lesson = db.relationship('Lesson', backref=db.backref('videos', lazy=True))
    created_by_user = db.relationship('User', backref=db.backref('created_videos', lazy=True))

    def __repr__(self):
        return f'<Video {self.title}>'

# Mô hình Material
class Material(db.Model):
    __tablename__ = 'materials'  # Tên bảng trong cơ sở dữ liệu

    material_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    affiliate_link = db.Column(db.String(255))
    image_url = db.Column(db.String(255))

    def __repr__(self):
        return f'<Material {self.name}>'

# Mô hình Material_Amount (liên kết giữa Materials và Videos)
class MaterialAmount(db.Model):
    __tablename__ = 'material_amount'  # Tên bảng trong cơ sở dữ liệu

    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'), primary_key=True)  # Khóa ngoại tới bảng 'materials'
    video_id = db.Column(db.Integer, db.ForeignKey('videos.video_id'), primary_key=True)  # Khóa ngoại tới bảng 'videos'
    amount = db.Column(db.Integer)

    # Mối quan hệ với bảng Material và Video
    material = db.relationship('Material', backref=db.backref('material_amounts', lazy=True))
    video = db.relationship('Video', backref=db.backref('material_amounts', lazy=True))

    def __repr__(self):
        return f'<MaterialAmount {self.amount}>'

# Mô hình Feedback
class Feedback(db.Model):
    __tablename__ = 'feedbacks'  # Tên bảng trong cơ sở dữ liệu

    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))  # Khóa ngoại tới bảng 'users'
    video_id = db.Column(db.Integer, db.ForeignKey('videos.video_id'))  # Khóa ngoại tới bảng 'videos'
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Mối quan hệ với bảng User và Video
    user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))
    video = db.relationship('Video', backref=db.backref('feedbacks', lazy=True))

    def __repr__(self):
        return f'<Feedback {self.rating} on Video {self.video_id}>'
# Mô hình profile
class UserProfile(db.Model):
    __tablename__ = 'user_profile'  # Tên bảng trong cơ sở dữ liệu

    profile_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # Khóa ngoại tới bảng 'users'
    full_name = db.Column(db.String(255), nullable=False)  # Tên đầy đủ
    avatar = db.Column(db.String(255))  # Hình ảnh đại diện
    address = db.Column(db.String(255))  # Địa chỉ
    followers_count = db.Column(db.Integer, default=0)  # Số lượng người theo dõi
    # Mối quan hệ với bảng User
    user = db.relationship('User', back_populates='profile')
    def __repr__(self):
        return f'<UserProfile {self.full_name} for {self.user.username}>'
