from nltk.tokenize import word_tokenize
from nltk.chunk import RegexpParser
from nltk.tag import pos_tag

def tokenize_sentence(sentence):
    data = []
    # Tách từ
    tokens = word_tokenize(sentence)

    # Gắn nhãn từ loại
    tags = pos_tag(tokens)

    # Định nghĩa pattern cho chunker
    chunker = RegexpParser("""
        NP: {<N.*>+}
        VP: {<V.*>+}
    """)

    # Áp dụng chunker để tách cụm động từ và cụm danh từ
    tree = chunker.parse(tags)
    for subtree in tree.subtrees():
        if subtree.label() == 'NP':
            noun_phrase = " ".join(word for word, tag in subtree.leaves())
            data.append(noun_phrase)
        elif subtree.label() == 'VP':
            verb_phrase = " ".join(word for word, tag in subtree.leaves())
            data.append(verb_phrase)
    return data