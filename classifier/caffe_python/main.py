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
    directories = ["/home/jonghoon/Desktop/datasets/data/fti_small_data/test_data/exe",
                   "/home/jonghoon/Desktop/datasets/data/fti_small_data/test_data/html",
                   "/home/jonghoon/Desktop/datasets/data/fti_small_data/test_data/hwp",
                   "/home/jonghoon/Desktop/datasets/data/fti_small_data/test_data/jpg",
                   "/home/jonghoon/Desktop/datasets/data/fti_small_data/test_data/mp3",
                   "/home/jonghoon/Desktop/datasets/data/fti_small_data/test_data/pdf",
                   "/home/jonghoon/Desktop/datasets/data/fti_small_data/test_data/png"]
    fragment_getter = Fragment(num_fragments=2000, file_types=file_types, directories=directories, fragment_size=4096)

    # Prepare caffe network
    net = caffe.Net("./deploy.prototxt", "./model.caffemodel", caffe.TEST)
    net.blobs["data"].reshape(1, 1, 256, 1)

    # Setup timer
    timer = Timer(name="Elapsed Time")

    # Classify
    total_fragments = 0
    correct_fragments = 0
    fragment, file_type = fragment_getter.get_fragment()
    while fragment is not None:
        total_fragments += 1

        timer.start()
        net.blobs["data"].data[...] = compute_bfd(fragment)
        result = net.forward()
        prob = result["prob"].tolist()[0]
        classified_type = file_groups[prob.index(max(prob))]
        timer.stop()

        if classified_type == file_type:
            correct_fragments += 1

        fragment, file_type = fragment_getter.get_fragment()

    print("Total Fragments: {}".format(total_fragments))
    print("Correct Classification: {} ({:.2f})%".format(correct_fragments,
                                                        correct_fragments / total_fragments * 100))
    timer.print()


if __name__ == "__main__":
    main()