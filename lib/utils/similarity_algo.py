# import re
# import editdistance # type: ignore[import-untyped]

# def preprocess_text(text):
#     text = text.lower()  # Convert to lowercase
#     text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
#     return text.strip()

# def token_similarity(tokens1, tokens2):
#     intersection = len(tokens1.intersection(tokens2))
#     union = len(tokens1.union(tokens2))
#     return intersection / union if union != 0 else 0

# def levenshtein_similarity(token1, token2):
#     distance = editdistance.eval(token1, token2)
#     max_len = max(len(token1), len(token2))
#     return 1 - (distance / max_len)

# def compare_fullnames(name1, name2):
#     name1_tokens = set(preprocess_text(name1).split())
#     name2_tokens = set(preprocess_text(name2).split())
    
#     token_sim = token_similarity(name1_tokens, name2_tokens)
    
#     levenshtein_sim = 0
#     for token1 in name1_tokens:
#         for token2 in name2_tokens:
#             levenshtein_sim += levenshtein_similarity(token1, token2)
#     levenshtein_sim /= len(name1_tokens) * len(name2_tokens)
    
#     return token_sim, levenshtein_sim

# def combine_similarity(token_sim, levenshtein_sim, token_weight=0.5, levenshtein_weight=0.5) -> float:
#     combined_sim = (token_sim * token_weight) + (levenshtein_sim * levenshtein_weight)
#     return combined_sim

# def compare_similarities(string1: str, string2: str, distance: float) -> bool:
#     token_sim, levenshtein_sim = compare_fullnames(string1, string2)
#     combined_sim = combine_similarity(token_sim, levenshtein_sim)
#     print(combined_sim)
#     return combined_sim >= distance



import re
import editdistance # type: ignore[import-untyped]

def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text.strip()

def token_similarity(tokens1, tokens2):
    intersection = len(tokens1.intersection(tokens2))
    union = len(tokens1.union(tokens2))
    return intersection / union if union != 0 else 0

def levenshtein_similarity(token1, token2):
    distance = editdistance.eval(token1, token2)
    max_len = max(len(token1), len(token2))
    return 1 - (distance / max_len)

def compare_texts(text1, text2, preferred_distance) -> bool:
    text1_tokens = set(preprocess_text(text1).split())
    text2_tokens = set(preprocess_text(text2).split())

    token_sim = token_similarity(text1_tokens, text2_tokens)

    levenshtein_sim = 0
    for token1 in text1_tokens:
        for token2 in text2_tokens:
            levenshtein_sim += levenshtein_similarity(token1, token2)
    levenshtein_sim /= len(text1_tokens) * len(text2_tokens)

    combined_sim = (token_sim + levenshtein_sim) / 2  # Combining using simple average
    print(combined_sim)
    return combined_sim >= preferred_distance

# Example usage
# text1 = "John Doe"
# text2 = "Doe John"
# preferred_distance = 0.7  # Adjust as needed

# is_similar = compare_texts(text1, text2, preferred_distance)
# print("Texts are similar:", is_similar)
