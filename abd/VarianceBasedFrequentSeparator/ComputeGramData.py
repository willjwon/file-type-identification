import numpy
import settings


def count_gram_frequency(gram_size, read_data, gram_frequency, introduced_grams):
    for index in range(len(read_data) - gram_size + 1):
        gram_value = int.from_bytes(read_data[index:(index + gram_size)], byteorder="big")
        gram_key = (gram_size, gram_value)
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

    return numpy.var(data)
