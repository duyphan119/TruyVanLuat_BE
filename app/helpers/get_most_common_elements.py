from collections import Counter


def get_most_common_elements(arr):
    counter = Counter(arr)
    most_common = counter.most_common()
    max_count = most_common[0][1] if most_common else 0
    most_common_elements = [elem for elem, count in most_common if count == max_count]
    return most_common_elements
