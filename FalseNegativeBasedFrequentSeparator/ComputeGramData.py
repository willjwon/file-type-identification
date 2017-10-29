import numpy
import settings


def count_gram_frequency(gram_size, read_data, gram_frequency, introduced_grams):
    grams_introduced_in_this_fragment = set()
    for index in range(len(read_data) - gram_size + 1):
        gram_value = int.from_bytes(read_data[index:(index + gram_size)], byteorder="big")
        gram_key = (gram_size, gram_value)
        if gram_key not in grams_introduced_in_this_fragment:
            grams_introduced_in_this_fragment.add(gram_key)
            if gram_key in gram_frequency:
                gram_frequency[gram_key] += 1
            else:
                gram_frequency[gram_key] = 1

        introduced_grams.add(gram_key)


def compute_gram_variance(gram_key, gram_frequency_data_by_types):
    data = []
    for file_type in settings.directory_path.keys():
        frequency_dict = gram_frequency_data_by_types[file_type]

        if gram_key in frequency_dict.keys():
            data.append(frequency_dict[gram_key])
        else:
            data.append(0)

    num_max_fragments = numpy.max(data)
    num_sum_fragments = numpy.sum(data)
    num_total_fragments = settings.num_fragments * len(settings.directory_path)
    try:
        return (settings.num_fragments - num_max_fragments) / (num_total_fragments - num_sum_fragments + 1)
    except ZeroDivisionError:
        return 1
