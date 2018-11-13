import lmdb
import caffe
import os
import numpy as np
from compute_bfd import compute_bfd
from caffe.proto import caffe_pb2
from fragment import Fragment


def main():
    # Setup Fragment
    file_types = ["exe", "html", "hwp", "jpg", "mp3", "pdf", "png"]
    file_groups = {"exe": 0,
                  "html": 1,
                  "hwp": 2,
                  "jpg": 3,
                  "mp3": 4,
                  "pdf": 5,
                  "png": 6}
    directories = ["/home/jonghoon/datasets/data/fti_data/train/exe",
                   "/home/jonghoon/datasets/data/fti_data/train/html",
                   "/home/jonghoon/datasets/data/fti_data/train/hwp",
                   "/home/jonghoon/datasets/data/fti_data/train/jpg",
                   "/home/jonghoon/datasets/data/fti_data/train/mp3",
                   "/home/jonghoon/datasets/data/fti_data/train/pdf",
                   "/home/jonghoon/datasets/data/fti_data/train/png"]
    step = 1000
    fragment_getter = Fragment(file_types=file_types, directories=directories)

    # LMDB Preparation
    if not os.path.exists("./lmdb"):
        os.makedirs("./lmdb")
    lmdb_env = lmdb.open("./lmdb", map_size=int(1e12))
    lmdb_txn = lmdb_env.begin(write=True)
    item_key = 0

    fragment, file_type, not_last = fragment_getter.get_fragment()
    while not_last:
        fragment_bfd = compute_bfd(fragment)
        datum = caffe.io.array_to_datum(fragment_bfd, file_groups[file_type])
        str_item_key = '{:0>8d}'.format(item_key).encode('ascii')
        lmdb_txn.put(str_item_key, datum.SerializeToString())

        item_key += 1
        if item_key % step == 0:
            lmdb_txn.commit()
            lmdb_txn = lmdb_env.begin(write=True)

        fragment, file_type, not_last = fragment_getter.get_fragment()

    lmdb_txn.commit()


if __name__ == "__main__":
    main()
