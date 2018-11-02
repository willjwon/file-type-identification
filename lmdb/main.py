# import lmdb
# import caffe
import os
import numpy as np
# from caffe.proto import caffe_pb2
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
    directories = ["/Users/barber/Data/fti_small_data/train_data/exe",
                   "/Users/barber/Data/fti_small_data/train_data/html",
                   "/Users/barber/Data/fti_small_data/train_data/hwp",
                   "/Users/barber/Data/fti_small_data/train_data/jpg",
                   "/Users/barber/Data/fti_small_data/train_data/mp3",
                   "/Users/barber/Data/fti_small_data/train_data/pdf",
                   "/Users/barber/Data/fti_small_data/train_data/png"]
    num_fragments = 10
    fragment_getter = Fragment(num_fragments=num_fragments,
                               file_types=file_types, directories=directories, fragment_size=4096)

    fragment, file_type = fragment_getter.get_fragment()
    while fragment is not None:
        # Do Something here
        fragment, file_type = fragment_getter.get_fragment()


if __name__ == "__main__":
    main()

#
# # LMDB Preparation
# if not os.path.exists("./lmdb"):
#     os.makedirs("./lmdb")
# lmdb_env = lmdb.open("./lmdb", map_size=int(1e12))
# lmdb_txn = lmdb_env.begin(write=True)
# item_key = 0
# datum = caffe_pb2.Datum()
#
# # Generate LMDB Value
# value = [0, 0, 0, 0,
#          0, 0, 0, 0,
#          1, 1, 1, 1,
#          1, 1, 1, 1]
# data = np.reshape(np.asarray(value), newshape=[1, 4, 4])
# label = 0
# datum = caffe.io.array_to_datum(data, label)
# str_item_key = '{:0>8d}'.format(item_key).encode('ascii')
# lmdb_txn.put(str_item_key, datum.SerializeToString())
# item_key += 1
#
# value = [0, 1, 1, 0,
#          1, 0, 0, 1,
#          1, 0, 0, 1,
#          0, 1, 1, 0]
# data = np.reshape(np.asarray(value), newshape=[1, 4, 4])
# label = 1
# datum = caffe.io.array_to_datum(data, label)
# str_item_key = '{:0>8d}'.format(item_key).encode('ascii')
# lmdb_txn.put(str_item_key, datum.SerializeToString())
# item_key += 1
#
# value = [0, 0, 1, 1,
#          0, 0, 1, 1,
#          1, 1, 0, 0,
#          1, 1, 0, 0]
# data = np.reshape(np.asarray(value), newshape=[1, 4, 4])
# label = 2
# datum = caffe.io.array_to_datum(data, label)
# str_item_key = '{:0>8d}'.format(item_key).encode('ascii')
# lmdb_txn.put(str_item_key, datum.SerializeToString())
# item_key += 1
#
# # Commit LMDB
# lmdb_txn.commit()
