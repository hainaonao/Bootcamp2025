from models import MaterialAmount

import requests

def extract_title_and_materials(input_text):
    url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    separation_prompt = {
        "contents": [{
            "parts": [{
                "text": (
                    f"Phân tích đoạn văn bản sau và trả về theo format yêu cầu:\n\n"
                    f"Văn bản: {input_text}\n\n"
                    f"Yêu cầu: Tách thành 2 phần - tiêu đề và danh sách vật liệu.\n"
                    f"Format trả về:\n"
                    f"TITLE: [tiêu đề bài học]\n"
                    f"MATERIALS: [danh sách vật liệu, mỗi vật liệu một dòng]"
                )
            }]
        }]
    }

    response = requests.post(url, json=separation_prompt, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code}")
    
    # Lấy phần văn bản trả về
    returned_text = response.json()['candidates'][0]['content']['parts'][0]['text']
    
    # Xử lý tách title và materials
    if 'MATERIALS:' in returned_text:
        parts = returned_text.split('MATERIALS:')
        title = parts[0].replace('TITLE:', '').strip()
        materials = [m.strip() for m in parts[1].strip().split('\n') if m.strip()]
    else:
        # Chỉ có tiêu đề, không có danh sách vật liệu
        title = returned_text.replace('TITLE:', '').strip()
        materials = []

    return title, materials

def jaccard_similarity_lists(list1, list2):
    set1 = set(item.strip().lower() for item in list1)
    set2 = set(item.strip().lower() for item in list2)
    
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    if not union:
        return 0.0  # Tránh chia cho 0 nếu cả hai đều rỗng
    
    return len(intersection) / len(union)

def ranking(input_text):
    title, materials = extract_title_and_materials(input_text)    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Vector hóa tiêu đề
    title_vec = model.encode(title).reshape(1, -1)
    title_similarities = []
    for v in video:
        # Tính độ tương đồng cosine giữa tiêu đề và các video
        description_vec = model.encode(v["description"]).reshape(1, -1)
        title_similarities.append(cosine_similarity(title_vec, description_vec))  # numpy array (N,)
    title_similarities = np.array(title_similarities)
    if materials:
        jaccard_similarities = []
        for v in video: 
            # Lấy danh sách vật liệu của video từ cơ sở dữ liệu
            material_records = MaterialAmount.query.filter_by(video_id=v).join(Material).all()
            
            # Lấy tên vật liệu từ quan hệ ORM
            materials2 = [m.material.name for m in material_records]
            
            # Tính Jaccard similarity và thêm vào danh sách
            jaccard_similarities.append(jaccard_similarity_lists(materials, materials2))

        # Chuyển jaccard_similarities thành numpy array để cộng được
        jaccard_similarities = np.array(jaccard_similarities)

        # Kết hợp hai loại độ tương đồng (có thể cân nhắc trọng số)
        similarities = title_similarities + jaccard_similarities  # numpy + numpy → OK

    else:
        similarities = title_similarities

    # Sắp xếp theo thứ tự tăng dần
    sorted_indices = np.argsort(similarities)
    sorted_videos = [v[i] for i in sorted_indices]
    return sorted_videos
