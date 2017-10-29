train_directory_path = {
    "mp3": "/Users/barber/Data/Research/File-type-identification/scraped-data/train_data/mp3",
    "hwp": "/Users/barber/Data/Research/File-type-identification/scraped-data/train_data/hwp",
    "pdf": "/Users/barber/Data/Research/File-type-identification/scraped-data/train_data/pdf",
    "jpg": "/Users/barber/Data/Research/File-type-identification/scraped-data/train_data/jpg",
    "png": "/Users/barber/Data/Research/File-type-identification/scraped-data/train_data/png"
}

validation_directory_path = {
    "mp3": "/Users/barber/Data/Research/File-type-identification/scraped-data/validation_data/mp3",
    "hwp": "/Users/barber/Data/Research/File-type-identification/scraped-data/validation_data/hwp",
    "pdf": "/Users/barber/Data/Research/File-type-identification/scraped-data/validation_data/pdf",
    "jpg": "/Users/barber/Data/Research/File-type-identification/scraped-data/validation_data/jpg",
    "png": "/Users/barber/Data/Research/File-type-identification/scraped-data/validation_data/png"
}

test_directory_path = {
    "mp3": "/Users/barber/Data/Research/File-type-identification/scraped-data/test_data/mp3",
    "hwp": "/Users/barber/Data/Research/File-type-identification/scraped-data/test_data/hwp",
    "pdf": "/Users/barber/Data/Research/File-type-identification/scraped-data/test_data/pdf",
    "jpg": "/Users/barber/Data/Research/File-type-identification/scraped-data/test_data/jpg",
    "png": "/Users/barber/Data/Research/File-type-identification/scraped-data/test_data/png"
}

output_path = "./test_output"

file_types = {
    "mp3": 0,
    "hwp": 1,
    "pdf": 2,
    "jpg": 3,
    "png": 4
}
num_groups = 5
max_grams = 3 

fragment_size_in_bytes = 4096
num_train_fragments_per_type = 100 
num_validation_fragments_per_type = 0
num_test_fragments_per_type = 0
num_fragments_per_csv = 500
