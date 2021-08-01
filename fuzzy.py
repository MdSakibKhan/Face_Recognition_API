from fuzzywuzzy import fuzz


def fuzzyCheck(actual, testData):
    score = fuzz.token_set_ratio(actual, testData)
    if score > 75:
        return score, 'S'
    return score, 'W'
