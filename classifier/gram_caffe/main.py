import caffe
from timer import Timer
from compute_bfd import compute_bfd
from gram_classifier import GramClassifier
from fragment import Fragment


def main():
    # Setup Fragment
    file_types = ["exe", "html", "hwp", "jpg", "mp3", "pdf", "png"]
    file_groups = {0: "exe",
                   1: "html",
                   2: "hwp",
                   3: "jpg",
                   4: "mp3",
                   5: "pdf",
                   6: "png"}
    directories = ["/home/jonghoon/Desktop/datasets/data/fti_small_data/test_data/exe",
                   "/home/jonghoon/Desktop/datasets/data/fti_small_data/test_data/html",
                   "/home/jonghoon/Desktop/datasets/data/fti_small_data/test_data/hwp",
                   "/home/jonghoon/Desktop/datasets/data/fti_small_data/test_data/jpg",
                   "/home/jonghoon/Desktop/datasets/data/fti_small_data/test_data/mp3",
                   "/home/jonghoon/Desktop/datasets/data/fti_small_data/test_data/pdf",
                   "/home/jonghoon/Desktop/datasets/data/fti_small_data/test_data/png"]
    fragment_getter = Fragment(num_fragments=10000, file_types=file_types, directories=directories, fragment_size=1000)

    # Prepare gram network
    gram_classifier = GramClassifier(fragment_size=1000)

    # Prepare caffe network
    net = caffe.Net("./deploy.prototxt", "./model.caffemodel", caffe.TEST)
    net.blobs["data"].reshape(1, 1, 256, 1)

    # Timer
    timer = Timer(name="Elapsed Time")

    # Classify
    gram_classified_fragments = 0
    gram_correct_fragments = 0
    nn_classified_fragments = 0
    nn_correct_fragments = 0
    classification_table = dict()
    for type1 in file_types:
        classification_table[type1] = dict()
        for type2 in file_types:
            classification_table[type1][type2] = 0

    fragment, file_type = fragment_getter.get_fragment()
    while fragment is not None:
        timer.start()
        # Try gram classification first
        classified_type = gram_classifier.classify(fragment)

        if classified_type is None:
            # Try caffe classification
            net.blobs["data"].data[...] = compute_bfd(fragment)
            result = net.forward()
            prob = result["prob"].tolist()[0]
            classified_type = file_groups[prob.index(max(prob))]
            timer.stop()

            nn_classified_fragments += 1
            if file_type == classified_type:
                nn_correct_fragments += 1
        else:
            timer.stop()

            gram_classified_fragments += 1
            if file_type == classified_type:
                gram_correct_fragments += 1

        classification_table[file_type][classified_type] += 1

        fragment, file_type = fragment_getter.get_fragment()

    total_fragments = gram_classified_fragments + nn_classified_fragments
    total_correct = gram_correct_fragments + nn_correct_fragments
    print()
    print("Gram: {}/{} ({:.2f}%), Accuracy: {:.2f}%".format(gram_classified_fragments,
                                                            total_fragments,
                                                            gram_classified_fragments / total_fragments * 100,
                                                            gram_correct_fragments / gram_classified_fragments * 100))
    print("MLP: {}/{} ({:.2f}%), Accuracy: {:.2f}%".format(nn_classified_fragments,
                                                           total_fragments,
                                                           nn_classified_fragments / total_fragments * 100,
                                                           nn_correct_fragments / nn_classified_fragments * 100))
    print("Total Accuracy: {:.2f}%".format(total_correct / total_fragments * 100))
    print("Accuracy Table:")
    print("\t" + "\t".join(file_types))
    for type1 in file_types:
        print("{}\t".format(type1), end="")
        for type2 in file_types:
            print("{:3.2f}%".format(classification_table[type1][type2] / 10000 * 100), end="\t")
        print()

    timer.print()


if __name__ == "__main__":
    main()
