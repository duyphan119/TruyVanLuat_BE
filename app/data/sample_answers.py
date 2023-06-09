data = {
    "chao_hoi": [
        "Xin chào, bạn có cần giúp đỡ về điều gì không?",
        "Chào bạn, tôi có thể giúp gì cho bạn ngày hôm nay?",
        "Hi, có gì tôi có thể giúp bạn?",
        "Xin chào! Bạn cần tôi giúp gì hôm nay?",
        "Hello! Bạn có câu hỏi hoặc yêu cầu gì tôi có thể giúp bạn?",
        "Chào bạn! Bạn muốn tìm hiểu về cái gì?",
        "Xin chào! Bạn đang tìm kiếm thông tin gì?"
    ],
    "tam_biet": [
        "Tạm biệt!",
        "Hẹn gặp lại!",
        "Chào tạm biệt!",
        "Rất vui được giúp bạn. Tạm biệt!",
        "Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi. Tạm biệt!",
        "Nếu bạn cần thêm thông tin, đừng ngần ngại liên hệ lại. Tạm biệt!",
        "Chúc bạn một ngày tốt lành. Tạm biệt!"
    ]
},
sample_answers = {key: value for key, value in data[0].items()}   

unclear_answers = [
    "Xin lỗi, tôi không hiểu câu hỏi của bạn. Bạn có thể cung cấp thông tin chi tiết hơn không?",
    "Tôi xin lỗi, nhưng tôi cần thêm thông tin để hiểu rõ hơn câu hỏi của bạn. Bạn có thể mô tả hoặc đặt câu hỏi cụ thể hơn được không?",
    "Xin lỗi, tôi cần bạn cung cấp thêm thông tin để tôi có thể giúp bạn. Bạn có thể nói rõ hơn về vấn đề bạn quan tâm không?",
    "Rất tiếc, tôi không thể trả lời câu hỏi vì thiếu thông tin. Bạn có thể cung cấp thêm chi tiết để tôi hiểu rõ hơn không?",
    "Xin lỗi, nhưng tôi không thể đưa ra câu trả lời chính xác vì câu hỏi của bạn không rõ ràng. Bạn có thể mô tả hoặc đặt câu hỏi cụ thể hơn được không?"
]