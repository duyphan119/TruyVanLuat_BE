import random
import string


def generate_random_string(length):
    # Lựa chọn ký tự từ các chữ cái và chữ số
    characters = string.ascii_letters + string.digits

    # Tạo chuỗi ngẫu nhiên từ các ký tự đã chọn
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string
