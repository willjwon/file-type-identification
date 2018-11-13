import caffe
from timer import Timer
from compute_bfd import compute_bfd
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
    directories = ["/home/jonghoon/Desktop/datasets/data/fti_data/test/exe",
                   "/home/jonghoon/Desktop/datasets/data/fti_data/test/html",
                   "/home/jonghoon/Desktop/datasets/data/fti_data/test/hwp",
                   "/home/jonghoon/Desktop/datasets/data/fti_data/test/jpg",
                   "/home/jonghoon/Desktop/datasets/data/fti_data/test/mp3",
                   "/home/jonghoon/Desktop/datasets/data/fti_data/test/pdf",
                   "/home/jonghoon/Desktop/datasets/data/fti_data/test/png"]
    fragment_getter = Fragment(file_types=file_types, directories=directories)

    # Prepare caffe network
    net = caffe.Net("./deploy.prototxt", "./model.caffemodel", caffe.TEST)
    net.blobs["data"].reshape(1, 1, 256, 1)

    # Setup timer
    timer = Timer(name="Elapsed Time")

    # Result checker
    total_fragments = 0
    correct_fragments = 0
    classification_table = dict()
    for type1 in file_types:
        classification_table[type1] = dict()
        for type2 in file_types:
            classification_table[type1][type2] = 0

    # Classify
    file_bytes, file_type, not_last = fragment_getter.get_fragment()
    while not_last:
        result_dict = dict()
        for file_type in file_types:
            result_dict[file_type] = 0

        timer.start()

        # fragment
        num_fragments = int(len(file_bytes) / 4096)
        for i in range(num_fragments):
            start_point = i * 4096
            fragment = file_bytes[start_point:start_point + 4096]

            net.blobs["data"].data[...] = compute_bfd(fragment)
            result = net.forward()
            prob = result["prob"].tolist()[0]
            fragment_classified_type = file_groups[prob.index(max(prob))]

            result_dict[fragment_classified_type] += 1

        classified_type = max(result_dict.items(), key=lambda x: result_dict[x])[0]
        timer.stop()

        total_fragments += 1
        if classified_type == file_type:
            correct_fragments += 1
        classification_table[file_type][classified_type] += 1

        file_bytes, file_type, not_last = fragment_getter.get_fragment()

    num_files = dict()
    for type1 in file_types:
        num_files[type1] = 0
        for type2 in file_types:
            num_files[type1] += classification_table[type1][type2]
    
    print()
    print("Accuracy: {:.2f}%".format(correct_fragments / total_fragments * 100))
    print("Accuracy Table:")
    print("\t" + "\t".join(file_types))
    for type1 in file_types:
        print("{}\t".format(type1), end="")
        for type2 in file_types:
            print("{:3.2f}%".format(classification_table[type1][type2] / num_files[type1] * 100), end="\t")
        print()

    timer.print()


if __name__ == "__main__":
    main()
