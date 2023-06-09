from slugify import slugify

def to_code(text):
    # Chuyển chuỗi thành slug
    slug = slugify(text)
    
    # Tách các từ trong slug và viết hoa chữ cái đầu
    words = slug.split("-")
    capitalized_words = [word.capitalize() for word in words]
    
    # Ghép lại các từ để tạo slug cuối cùng
    final_slug = "".join(capitalized_words)
    
    return final_slug