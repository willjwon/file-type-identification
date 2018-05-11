directory_path = {
    "mp3": "/Users/barber/Data/Research/File-type-identification/scraped-data/train_data/mp3",
    "hwp": "/Users/barber/Data/Research/File-type-identification/scraped-data/train_data/hwp",
    "pdf": "/Users/barber/Data/Research/File-type-identification/scraped-data/train_data/pdf",
    "jpg": "/Users/barber/Data/Research/File-type-identification/scraped-data/train_data/jpg",
    "png": "/Users/barber/Data/Research/File-type-identification/scraped-data/train_data/png"
}

fragment_size_in_bytes = 4096
num_fragments = 6000

start_gram = 3
finish_gram = 3

false_negative_level_to_pick = 0.17

# -------- 2-gram -------
# fp
# 0.5   0.45    0.4     0.35    0.3
# 305   89      22      2       2

# fn
# 0.18    0.17    0.16    0.15    0.14    0.13
# 1236    283     77      21      8       4

# fp   fn       #sep #added
# 0.45 0.17  => 291 (+8)
# 0.5  0.17  => 378 (+95)
# ----------------------
