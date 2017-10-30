train_directory_path = {
    "html": "/Users/kyang/Desktop/scraped-data/train_data/html",
    "exe": "/Users/kyang/Desktop/scraped-data/train_data/exe",
    "mp3": "/Users/kyang/Desktop/scraped-data/train_data/mp3",
    "hwp": "/Users/kyang/Desktop/scraped-data/train_data/hwp",
    "pdf": "/Users/kyang/Desktop/scraped-data/train_data/pdf",
    "jpg": "/Users/kyang/Desktop/scraped-data/train_data/jpg",
    "png": "/Users/kyang/Desktop/scraped-data/train_data/png"
}

validation_directory_path = {
    "html": "/Users/kyang/Desktop/scraped-data/validation_data/html",
    "exe": "/Users/kyang/Desktop/scraped-data/validation_data/exe",
    "mp3": "/Users/kyang/Desktop/scraped-data/validation_data/mp3",
    "hwp": "/Users/kyang/Desktop/scraped-data/validation_data/hwp",
    "pdf": "/Users/kyang/Desktop/scraped-data/validation_data/pdf",
    "jpg": "/Users/kyang/Desktop/scraped-data/validation_data/jpg",
    "png": "/Users/kyang/Desktop/scraped-data/validation_data/png"
}

test_directory_path = {
    "html": "/Users/kyang/Desktop/scraped-data/test_data/html",
    "exe": "/Users/kyang/Desktop/scraped-data/test_data/exe",
    "mp3": "/Users/kyang/Desktop/scraped-data/test_data/mp3",
    "hwp": "/Users/kyang/Desktop/scraped-data/test_data/hwp",
    "pdf": "/Users/kyang/Desktop/scraped-data/test_data/pdf",
    "jpg": "/Users/kyang/Desktop/scraped-data/test_data/jpg",
    "png": "/Users/kyang/Desktop/scraped-data/test_data/png"
}

output_path = "./test_output"

file_types = {
    "html": 0,
    "exe": 1,
    "mp3": 2,
    "hwp": 3,
    "pdf": 4,
    "jpg": 5,
    "png": 6
}
num_groups = 7

fragment_size_in_bytes = 4096

num_train_fragments_per_type = 10000
num_validation_fragments_per_type = 2000
num_test_fragments_per_type = 4000
num_fragments_per_csv = 100