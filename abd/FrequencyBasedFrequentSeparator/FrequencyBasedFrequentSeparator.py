import pickle
import settings
import os
import copy
import collections
from File import File
from PrintProgress import print_progress

def get_common_gram(n, gram_list):
    gram_hex_list = {}

    # This is just for showing you how this works
    # Please remove this after you make pickle, csv data.
    for length in sorted(gram_list):
        for gram, count in gram_list[length].most_common(10):
            gram_hex_listprint(gram[:length], count)
        print('')
# gram_list contains each counter for each gram length
# For example, if you want to get the most frequent 30 2-grams,
# gram_list[2].most_common(30) will return you 30 (2-gram, count) pairs
# If you want a sorted list, use "sorted(gram_list)"
def main():
    num_fragments_done = 0
    num_total_fragments = settings.num_fragments \
                          * len(settings.directory_path) \
                          * (settings.max_length - settings.min_length + 1)
    lengths = range(settings.min_length, settings.max_length + 1)
    gram_list = {length: collections.Counter() for length in lengths}

    for length in lengths:
        for file_type in settings.directory_path.keys():
            file = File(settings.directory_path[file_type])

            fragment_data = file.read(settings.fragment_size_in_bytes)
            fragments_processed = 0
            while fragment_data is not None and fragments_processed < settings.num_fragments:
                gram_data = zip(*[fragment_data[i:] for i in range(length)])

                for gram in gram_data:
                    gram_list[length][gram] += 1

                fragments_processed += 1
                fragment_data = file.read(settings.fragment_size_in_bytes)

                num_fragments_done += 1
                print_progress(num_fragments_done, num_total_fragments)

    print_progress(num_fragments_done, num_total_fragments)

    # This is just for showing you how this works
    # Please remove this after you make pickle, csv data.
    for length in sorted(gram_list):
        print('----- {} most common {}-grams -----'.format(10, length))
        for gram, count in gram_list[length].most_common(10):
            print(gram, count)

if __name__ == "__main__":
    main()
