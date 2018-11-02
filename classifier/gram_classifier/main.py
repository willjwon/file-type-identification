from fragment import Fragment
from gram_classifier import GramClassifier


def main():
    # Setup Fragment
    file_types = ["exe", "html", "hwp", "jpg", "mp3", "pdf", "png"]
    directories = ["/Users/barber/Data/fti_small_data/test_data/exe",
                   "/Users/barber/Data/fti_small_data/test_data/html",
                   "/Users/barber/Data/fti_small_data/test_data/hwp",
                   "/Users/barber/Data/fti_small_data/test_data/jpg",
                   "/Users/barber/Data/fti_small_data/test_data/mp3",
                   "/Users/barber/Data/fti_small_data/test_data/pdf",
                   "/Users/barber/Data/fti_small_data/test_data/png"]
    fragment_getter = Fragment(num_fragments=2000, file_types=file_types, directories=directories, fragment_size=4096)

    gram_classifier = GramClassifier(fragment_size=4096)

    total_fragments = 0
    classified_fragments = 0
    correct_fragments = 0
    fragment, file_type = fragment_getter.get_fragment()
    while fragment is not None:
        total_fragments += 1

        classified_type = gram_classifier.classify(fragment)
        if classified_type is None:
            fragment, file_type = fragment_getter.get_fragment()
            continue

        classified_fragments += 1
        if classified_type == file_type:
            correct_fragments += 1

        fragment, file_type = fragment_getter.get_fragment()

    print("Total Fragments: {}".format(total_fragments))
    print("Classified Fragments: {} ({:.2f}%)".format(classified_fragments,
                                                      classified_fragments / total_fragments * 100))
    print("Correct Classification: {} ({:.2f})%".format(correct_fragments,
                                                       correct_fragments / classified_fragments * 100))


if __name__ == "__main__":
    main()
