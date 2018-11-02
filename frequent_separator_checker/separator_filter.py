class SeparatorFilter:
    def __init__(self, file_types, frequent_separators):
        self.separators_table = dict()
        self.file_types = file_types
        for file_type in file_types:
            self.separators_table[file_type] = dict()
            for gram, separators in frequent_separators.items():
                self.separators_table[file_type][gram] = dict()
                for separator in separators:
                    self.separators_table[file_type][gram][separator] = 0

        self.max_gram = max(frequent_separators.keys())

    def count_fragment(self, fragment, file_type):
        for gram_size in range(2, self.max_gram + 1):
            gram_set = set()
            for i in range(len(fragment) - gram_size + 1):
                gram_set.add(fragment[i:i + gram_size])
            for gram in gram_set:
                if gram in self.separators_table[file_type][gram_size].keys():
                    self.separators_table[file_type][gram_size][gram] += 1

    def filter_grams(self, threshold):
        filtered_grams = dict()
        for gram_size in range(2, self.max_gram + 1):
            filtered_grams[gram_size] = set()
            for gram in self.separators_table[self.file_types[0]][gram_size].keys():
                value = []
                for file_type in self.file_types:
                    value.append(self.separators_table[file_type][gram_size][gram])

                probability = max(value) / sum(value)
                if probability >= threshold:
                    for file_type in self.file_types:
                        if self.separators_table[file_type][gram_size][gram] == max(value):
                            filtered_grams[gram_size].add((gram, file_type, probability))
                            break

        filtered_grams = {k: v for k, v in filtered_grams.items() if len(v) != 0}
        return filtered_grams

    @staticmethod
    def change_filtered_gram_form(filtered_grams):
        reformatted_grams = dict()
        for gram_size, grams in filtered_grams.items():
            reformatted_grams[gram_size] = dict()
            for gram, file_type, _ in grams:
                reformatted_grams[gram_size][gram] = file_type

        return reformatted_grams

    def print_gram_type_statistics(self, formatted_grams):
        stat = dict()
        for file_type in self.file_types:
            stat[file_type] = 0

        total_count = 0
        for grams in formatted_grams.values():
            for file_type in grams.values():
                stat[file_type] += 1
                total_count += 1

        for file_type, count in stat.items():
            print("{}: {} ({:.2f}%".format(file_type, count, count / total_count * 100))
