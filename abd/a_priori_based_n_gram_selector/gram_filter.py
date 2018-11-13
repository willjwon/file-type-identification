import operator


class GramFilter:
    def __init__(self):
        self.grams = dict()

    def add_frequent_grams(self, frequent_grams):
        grams_to_add = frequent_grams.copy()
        max_frequency = max(grams_to_add.values())
        for gram, frequency in grams_to_add.items():
            self.grams[gram] = frequency / max_frequency

    def filter_top_n_grams(self, n):
        selected_grams = dict()
        sorted_grams = sorted(self.grams.items(), key=operator.itemgetter(1), reverse=True)
        for i in range(min(n, len(sorted_grams))):
            gram, _ = sorted_grams[i]
            gram_len = len(gram)
            if gram_len in selected_grams:
                selected_grams[gram_len].append(gram)
            else:
                selected_grams[gram_len] = [gram]
        return selected_grams
