from flask import render_template, request, redirect, url_for, flash, session, jsonify,g
from models import User, Video, Lesson, Material,MaterialAmount,Feedback, UserProfile
from datetime import datetime
from datetime import timezone
from fuzzywuzzy import process 
from models import db
from sklearn.metrics.pairwise import cosine_similarity
from functools import wraps
from urllib.parse import urlparse, urljoin
from sqlalchemy import func
import numpy as np
from sentence_transformers import SentenceTransformer
import re
import requests
import json
import humanize
# API GEMINI
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
GEMINI_API_KEY = "AIzaSyAeJV3HJq8UlIBn42Y8qTvr5XyawIfOOlI"  
# Tính năng giải thích
def replace_star_in_lines(text):
    result = []
    star_found = False 
    for char in text:
        if char == '*':
            if not star_found:
                star_found = True  
                continue  
            else:
                result.append('<br>')  
        else:
            result.append(char)  
    return ''.join(result)

def format_explanation(explanation):
    explanation = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", explanation)
    sections = {}
    definition_match = re.search(r"Định nghĩa:(.*?)(Giải thích khoa học|Ví dụ thực tế|Tổng kết|$)", explanation, re.DOTALL)
    if definition_match:
        sections['definition'] = definition_match.group(1).strip()
    else:
        sections['definition'] = "Không có định nghĩa"
    scientific_explanation_match = re.search(r"Giải thích khoa học:(.*?)(Ví dụ thực tế|Tổng kết|$)", explanation, re.DOTALL)
    if scientific_explanation_match:
        sections['scientific_explanation'] = scientific_explanation_match.group(1).strip()
    else:
        sections['scientific_explanation'] = "Không có giải thích khoa học"
    example_match = re.search(r"Ví dụ thực tế:(.*?)(Tổng kết|$)", explanation, re.DOTALL)
    if example_match:
        sections['example'] = example_match.group(1).strip()
    else:
        sections['example'] = "Không có ví dụ thực tế"
    summary_match = re.search(r"Tổng kết:(.*)", explanation, re.DOTALL)
    if summary_match:
        sections['summary'] = summary_match.group(1).strip()
    else:
        sections['summary'] = "Không có tổng kết"
    print("Đây là section:",sections)
    for key in sections:
        sections[key] = replace_star_in_lines(sections[key])
    return sections

def get_gemini_explanation(title, description):
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            f"Giải thích tính khoa học về hoạt động STEM dưới đây, chỉ trả lời theo các phần cần thiết:\n\n"
                            f"Tiêu đề: {title}\nMô tả: {description}\n\n"
                            "Cấu trúc yêu cầu:\n"
                            "Định nghĩa: Cung cấp giải thích ngắn gọn về nguyên lý khoa học liên quan.\n"
                            "Giải thích khoa học: Giải thích chi tiết hơn về nguyên lý khoa học, dựa trên sách giáo khoa.\n"
                            "Ví dụ thực tế: Cung cấp một hoặc nhiều ví dụ liên quan.\n"
                            "Tổng kết: Tóm tắt lại những điểm chính về nguyên lý khoa học và ứng dụng của nó.")
                    }
                ]
            }
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        response_data = response.json()  
        content = response_data['candidates'][0]['content']['parts'][0]['text']
        formatted_explanation = format_explanation(content)
        return formatted_explanation
    else:
        print(f"API Error: {response.status_code} - {response.text}")
        return f"Lỗi khi gọi API Gemini: {response.status_code} - {response.text}"

_REQUIRED_KEYS = {"definition", "scientific_explanation", "example", "summary"}

def _read_explanation_from_principle(raw: str):
    """Ưu tiên đọc JSON; nếu không phải JSON thì thử parse theo format cũ."""
    raw = (raw or "").strip()
    if not raw:
        return None
    # Thử JSON
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict):
            data = obj.get("data") if isinstance(obj.get("data"), dict) else obj
            if _REQUIRED_KEYS.issubset(data.keys()):
                return data
    except Exception:
        pass
    # Thử chuỗi text cũ -> tách section
    try:
        return format_explanation(raw)
    except Exception:
        return None

def load_video_data():
    with open('embedded_titles.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def find_closest_title(query_title, video_data):
    titles = [video['title'] for video in video_data]
    best_match = process.extractOne(query_title, titles)  
    return best_match[0] if best_match else None
# Chức năng search (8/8)
_sbert_model = None
def _get_sbert():
    global _sbert_model
    if _sbert_model is None:
        _sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
    return _sbert_model

def extract_title_and_materials(input_text):
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    separation_prompt = {
        "contents": [{
            "parts": [{
                "text": (
                    "Phân tích đoạn văn bản sau và trả về theo format yêu cầu:\n\n"
                    f"Văn bản: {input_text}\n\n"
                    "Yêu cầu: Tách thành 2 phần - tiêu đề  và danh sách vật liệu.\n"
                    "Format trả về:\n"
                    "TITLE: [tiêu đề bài học]\n"
                    "MATERIALS: [danh sách vật liệu, mỗi vật liệu một dòng]"
                )
            }]
        }]
    }
    try:
        response = requests.post(url, json=separation_prompt, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception:
        return input_text.strip(), []
    try:
        returned_text = response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        return input_text.strip(), []
    if 'MATERIALS:' in returned_text:
        parts = returned_text.split('MATERIALS:')
        title = parts[0].replace('TITLE:', '').strip()
        materials = [m.strip() for m in parts[1].strip().split('\n') if m.strip()]
    else:
        title = returned_text.replace('TITLE:', '').strip()
        materials = []
    return title, materials

def jaccard_similarity_lists(list1, list2):
    set1 = set(item.strip().lower() for item in list1 if item)
    set2 = set(item.strip().lower() for item in list2 if item)
    if not set1 and not set2:
        return 0.0
    return len(set1 & set2) / len(set1 | set2)

def _video_material_names(video_id: int):
    records = (MaterialAmount.query
               .filter_by(video_id=video_id)
               .join(Material, Material.material_id == MaterialAmount.material_id)
               .all())
    names = []
    for r in records:
        mat = getattr(r, "material", None)
        if mat:
            names.append(getattr(mat, "name", None))
    return [n for n in names if n]


# Phân quyền các trang (13/8)
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target or ""))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get('user_id'):
            flash("Bạn cần đăng nhập để tiếp tục.", "warning")
            return redirect(url_for('login', next=request.url))
        return view(*args, **kwargs)
    return wrapped

def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get('user_id'):
                flash("Bạn cần đăng nhập để tiếp tục.", "warning")
                return redirect(url_for('login', next=request.url))
            u = User.query.get(session['user_id'])
            if not u or u.role not in roles:
                flash("Bạn không có quyền truy cập.", "danger")
                return redirect(url_for('home'))
            return view(*args, **kwargs)
        return wrapped
    return decorator



# RENDER LÊN CÁC TRANG **************************************************************************************************************************
def init_routes(app):
    @app.after_request
    def add_no_cache_headers(response):
        # tránh trình duyệt cache trang private, sau logout bấm Back sẽ không hiện lại
        response.headers['Cache-Control'] = 'no-store'
        return response
    @app.before_request
    def load_current_user():
        g.user = User.query.get(session['user_id']) if session.get('user_id') else None
    @app.context_processor
    def inject_user():
        # Dùng trong template: {% if current_user %} ...
        return {"current_user": g.user}
    
    @app.route('/')
    def index():
        return redirect(url_for('home')) 
    # Đăng nhập
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()
            if user and user.password == password: 
                session.pop('email', None)
                session.pop('user_id', None)
                session['email'] = user.email
                session['user_id'] = user.user_id  
                session['username'] = user.username

                if user.role == 'admin':
                    return redirect(url_for('admin_page')) 
                else:
                    return redirect(url_for('home'))  
            else:
                flash('Thông tin đăng nhập không hợp lệ, vui lòng thử lại.', 'danger')

        return render_template('Login2.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            full_name = (request.form.get('fullName') or '').strip()
            email = (request.form.get('email') or '').strip().lower()
            password = request.form.get('password') or ''
            confirm_password = request.form.get('confirmPassword') or ''

            # Validate cơ bản
            if not full_name:
                flash('Vui lòng nhập họ và tên', 'danger')
                return render_template('Register.html')
            if not email:
                flash('Vui lòng nhập email', 'danger')
                return render_template('Register.html')
            if password != confirm_password:
                flash('Mật khẩu xác nhận không khớp', 'danger')
                return render_template('Register.html')
            if len(password) < 8:
                flash('Mật khẩu phải có ít nhất 8 ký tự', 'danger')
                return render_template('Register.html')

            # Email đã tồn tại?
            if User.query.filter_by(email=email).first():
                flash('Email đã được sử dụng. Vui lòng dùng email khác.', 'danger')
                return render_template('Register.html')

            # Tạo username tự động từ email + chống trùng
            base_username = email.split('@')[0]
            # (tuỳ chọn) làm sạch: chỉ giữ a-z0-9 và dấu gạch
            import re
            base_username = re.sub(r'[^a-z0-9\-_.]+', '', base_username.lower()) or 'user'
            username = base_username
            i = 1
            while User.query.filter_by(username=username).first() is not None:
                username = f"{base_username}{i}"
                i += 1

            # Tạo user mới (role mặc định student) — khớp schema User hiện tại
            new_user = User(
                username=username,
                password=password,   # (sau có thể nâng cấp hash)
                email=email,
                role='teacher'
            )
            db.session.add(new_user)
            db.session.commit()

            # Tạo UserProfile với full_name — khớp schema
            profile = UserProfile(
                user_id=new_user.user_id,
                full_name=full_name
            )
            db.session.add(profile)
            db.session.commit()

            flash('Đăng ký thành công. Bạn có thể đăng nhập ngay bây giờ!', 'success')
            return redirect(url_for('login'))

        return render_template('Register.html')

    @app.route('/logout', methods=['GET'])
    def logout():
        session.clear()
        flash("Bạn đã đăng xuất.", "success")
        return redirect(url_for('login'))
    # Trang admin
    @app.route('/admin')
    @role_required('admin')
    def admin_page():
        return render_template('Admin.html')  

    # Trang chủ
    @app.route('/home')
    def home():
        username = session.get('username')  
        user_id = session.get('user_id')   
        top_videos = Video.query.order_by(Video.view.desc()).limit(6).all()
        return render_template('Home.html', username=username, user_id=user_id, videos = top_videos) 
    
    #Phần đánh giá (Update 16/8)
    @app.post('/api/rate/<int:video_id>')
    @login_required
    def api_rate(video_id):
        data = request.get_json(silent=True) or {}

        # --- Lấy & validate input ---
        try:
            rating = int(data.get('rating', 0))
        except ValueError:
            rating = 0
        comment = (data.get('comment') or '').strip()

        if rating < 1 or rating > 5:
            return jsonify({"ok": False, "error": "Rating phải từ 1 đến 5"}), 400
        if len(comment) > 1000:
            return jsonify({"ok": False, "error": "Bình luận quá dài (<=1000 ký tự)"}), 400

        # --- Upsert Feedback ---
        fb = Feedback.query.filter_by(user_id=session['user_id'], video_id=video_id).first()
        if fb:
            # cập nhật sao
            fb.rating = rating
            # nếu client gửi khóa 'comment' thì cập nhật; tránh ghi đè ngoài ý muốn
            if 'comment' in data:
                fb.comment = comment or None
            # nếu model có created_at mà đang None, set thủ công
            if getattr(fb, 'created_at', None) is None:
                fb.created_at = datetime.utcnow()
        else:
            fb = Feedback(
                user_id=session['user_id'],
                video_id=video_id,
                rating=rating,
                comment=comment or None,
                created_at=datetime.utcnow()  # nếu cột có default thì dòng này không bắt buộc
            )
            db.session.add(fb)

        db.session.commit()

        # --- Tính lại thống kê ---
        avg, cnt = db.session.query(
            func.avg(Feedback.rating),
            func.count(Feedback.feedback_id)
        ).filter(Feedback.video_id == video_id).first()

        rows = (db.session.query(Feedback.rating, func.count(Feedback.feedback_id))
                .filter(Feedback.video_id == video_id)
                .group_by(Feedback.rating)
                .all())
        hist = {i: 0 for i in range(1, 6)}
        for r, c in rows:
            try:
                ri = int(r)
                if 1 <= ri <= 5:
                    hist[ri] = int(c)
            except:
                pass

        return jsonify({
            "ok": True,
            "my_rating": rating,
            "avg": round(float(avg or 0), 2),
            "count": int(cnt or 0),
            "hist": hist,
            "review": {
                "rating": rating,
                "comment": fb.comment or ""
            }
        })


    # Trang VideoSingle
    @app.route('/video/<int:video_id>')
    def video_single(video_id):
        video = Video.query.get(video_id)
        if not video:
            flash("Video không tồn tại.", "danger")
            return redirect(url_for('home'))
        materials = MaterialAmount.query.filter_by(video_id=video_id).join(Material).all()
        humanize.i18n.activate('vi_VN')
        time_diff = humanize.naturaltime(datetime.now() - video.created_at)
        
        # ==== NEW: đọc cache từ cột videos.principle trước ====
        explanation = _read_explanation_from_principle(video.principle)

        if explanation is None:
            # (giữ nguyên các dòng cũ trong nhánh else này)
            sgk_data = load_video_data()
            model = SentenceTransformer('all-MiniLM-L6-v2')
            query = video.description
            query_vec = model.encode(query).reshape(1, -1)
            doc_embeddings = np.array([d["embedding"] for d in sgk_data])
            similarities = cosine_similarity(query_vec, doc_embeddings)[0]
            best_idx = int(np.argmax(similarities))
            matched_doc = sgk_data[best_idx]
            explanation = get_gemini_explanation(video.title, matched_doc['content'])
            print(video.title, matched_doc['title'], matched_doc['content'])
            print(explanation)

            # LƯU cache (JSON) vào cột principle để lần sau không gọi Gemini nữa
            try:
                video.principle = json.dumps(explanation, ensure_ascii=False)
                db.session.commit()
            except Exception:
                db.session.rollback()

                # Up date đánh giá (16/8)
        avg, cnt = db.session.query(
            func.avg(Feedback.rating),
            func.count(Feedback.feedback_id)
        ).filter(Feedback.video_id == video_id).first()
        avg_rating = round(float(avg or 0), 2)
        rating_count = int(cnt or 0)

        # Lấy rating của chính user (nếu đăng nhập)
        my_rating = 0
        if session.get('user_id'):
            fb = Feedback.query.filter_by(user_id=session['user_id'], video_id=video_id).first()
            if fb:
                my_rating = fb.rating

        # >>> THÊM ĐOẠN NÀY: tính histogram 1..5 sao
        rows = db.session.query(
            Feedback.rating,
            func.count(Feedback.feedback_id)
        ).filter(Feedback.video_id == video_id).group_by(Feedback.rating).all()

        star_hist = {i: 0 for i in range(1, 6)}
        for r, c in rows:
            try:
                r_int = int(r)
                if 1 <= r_int <= 5:
                    star_hist[r_int] = int(c)
            except (TypeError, ValueError):
                pass
        # star_hist đã có dạng {1: x, 2: y, 3: z, 4: a, 5: b}
        max_star_count = max(star_hist.values()) if any(star_hist.values()) else 1
        # <<< HẾT ĐOẠN THÊM
        humanize.i18n.activate('vi_VN')

        reviews_q = (db.session.query(Feedback, User.username)
                    .join(User, User.user_id == Feedback.user_id)
                    .filter(Feedback.video_id == video_id)
                    .order_by(Feedback.created_at.desc(), Feedback.feedback_id.desc())
                    .limit(50)  # tuỳ bạn
                    .all())

        def _human(dt):
            try:
                return humanize.naturaltime(datetime.now() - dt)
            except Exception:
                return ""

        reviews = []
        for fb, uname in reviews_q:
            reviews.append({
                "user": uname,
                "rating": int(fb.rating or 0),
                "comment": fb.comment or "",
                "created_at_human": _human(fb.created_at) if getattr(fb, 'created_at', None) else "",
                "created_at_iso": fb.created_at.isoformat() if getattr(fb, 'created_at', None) else ""
            })
        return render_template('VideoSingle.html', video=video, materials=materials, time_diff=time_diff, explanation=explanation,avg_rating=avg_rating,
        rating_count=rating_count,
        my_rating=my_rating,star_hist=star_hist,
        max_star_count=max_star_count,
        reviews=reviews)
    
    # Trang Khám phá
    @app.route('/allvideo', methods=['GET'])
    def all_videos():
        category = request.args.get('category', 'all')  
        if category == 'all':
            lessons = Lesson.query.all()
        else:
            lessons = Lesson.query.filter(Lesson.title.like(f'%{category}%')).all()
        lesson_videos = {}
        for lesson in lessons:
            videos = Video.query.filter_by(lesson_id=lesson.lesson_id).order_by(Video.view.desc()).limit(3).all()
            lesson_videos[lesson.title] = videos
        return render_template('AllVideo.html', lesson_videos=lesson_videos)
    
    # Lọc trang khám phá
    @app.route('/allvideodetail/<category>', methods=['GET'])
    def all_video_details(category):
        lessons = Lesson.query.filter(Lesson.title.like(f'%{category}%')).all()
        lesson_videos = {}
        for lesson in lessons:
            videos = Video.query.filter_by(lesson_id=lesson.lesson_id).order_by(Video.view.desc()).all()
            lesson_videos[lesson.title] = videos
        return render_template('AllVideoDetail.html', lesson_videos=lesson_videos, category=category)

    # Trang Userdashboard
    @app.route('/userdashboard')
    @login_required
    def user_dashboard():
        username = session.get('username')
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        if user:
            user_profile = UserProfile.query.filter_by(user_id=user_id).first()
        else:
            flash("Người dùng không tồn tại.", "danger")
            return redirect(url_for('home'))
        return render_template('UserDashboard.html', user=user, user_profile=user_profile)
    
    # Trang kết quả tìm kiếm (8/8)
    @app.route('/search', methods=['GET'])
    def search():
        # 1) Lấy input
        raw_q = (request.args.get('q') or '').strip()
        if not raw_q:
            return render_template('SearchResult.html',
                                   query=raw_q, total=0, results=[])

        # 2) Dùng Gemini tách (title, materials)
        parsed_title, parsed_materials = extract_title_and_materials(raw_q)

        # 3) Lấy candidates từ DB (lọc sơ bộ theo title/description để giảm tải)
        candidates = Video.query.limit(200).all()
        if not candidates:
            return []

        # 4) SBERT encode: tiêu đề (hoặc raw_q) vs mô tả/tựa video
        model = _get_sbert()
        query_text = parsed_title or raw_q
        query_vec = model.encode([query_text])              # shape (1, d)
        desc_list = [(v.description or v.title or '') for v in candidates]
        desc_vecs = model.encode(desc_list)                 # shape (N, d)

        # 5) Cosine similarity theo mô tả
        cosims = cosine_similarity(query_vec, desc_vecs)[0] # (N,)

        # 6) Nếu có materials → cộng thêm điểm Jaccard
        if parsed_materials:
            jaccs = []
            for v in candidates:
                vid = getattr(v, 'video_id', getattr(v, 'id', None))
                mats2 = _video_material_names(vid)
                jaccs.append(jaccard_similarity_lists(parsed_materials, mats2))
            jaccs = np.array(jaccs, dtype=float)
            scores = cosims + jaccs  # có thể thêm trọng số nếu muốn
        else:
            scores = cosims

        # 7) Sắp xếp theo điểm giảm dần
        order = np.argsort(-scores)
        top = [candidates[i] for i in order[:50]]

        # 8) Chuẩn hoá dữ liệu trả ra template
        results = top
        
        return render_template('SearchResult.html',
                               query=raw_q,
                               parsed_title=parsed_title,
                               parsed_materials=parsed_materials,
                               total=len(results),
                               results=results)
    

    