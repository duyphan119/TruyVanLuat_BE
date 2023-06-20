from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

# Dữ liệu huấn luyện
train_sentences = ["Đường cao tốc là gì",
                   "Các vi phạm liên quan",
                   "Đi bộ trên đường cao tốc bị phạt gì",
                   "Cách khắc phục"]

train_labels = ["xem_khai_niem", "liet_ke_vi_pham", "xem_vi_pham", "khac_phuc"]

# Tiền xử lý dữ liệu
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(train_sentences)

# Xây dựng mô hình
classifier = LinearSVC()
classifier.fit(X_train, train_labels)

# Dữ liệu kiểm thử
test_sentence = "Đường ưu tiên là gì"

# Tiền xử lý dữ liệu kiểm thử
X_test = vectorizer.transform([test_sentence])

# Dự đoán intent
predicted_label = classifier.predict(X_test)

# In kết quả
print("Intent dự đoán:", predicted_label)

test_sentence = "Liệt kê"

# Tiền xử lý dữ liệu kiểm thử
X_test = vectorizer.transform([test_sentence])

# Dự đoán intent
predicted_label = classifier.predict(X_test)

# In kết quả
print("Intent dự đoán:", predicted_label)
