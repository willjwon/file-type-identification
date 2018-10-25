import settings

_zeros = ', '.join(["0"] * (len(settings.file_path) + 1))


def create_database(connection):
    file_types = ", ".join(["{} INTEGER".format(file_type) for file_type in settings.file_path.keys()])
    query_string = "CREATE TABLE IF NOT EXISTS frequency " \
                   "(gram INTEGER, gram_value INTEGER, maximum INTEGER, {}, PRIMARY KEY (gram, gram_value))"\
        .format(file_types)
    connection.cursor().execute(query_string)
    connection.commit()


def remove_database(connection):
    query_string = "DROP TABLE IF EXISTS frequency"
    connection.cursor().execute(query_string)
    connection.commit()


def increase_new_gram_data(connection, gram, gram_value, file_type):
    query_string = "INSERT OR IGNORE INTO frequency VALUES ({}, {}, {})".format(gram, gram_value, _zeros)
    connection.cursor().execute(query_string)

    query_string = "UPDATE frequency SET {} = {} + 1 WHERE gram = {} AND gram_value = {}" \
        .format(file_type, file_type, gram, gram_value)
    connection.cursor().execute(query_string)

    connection.commit()


def pick_by_maximum(connection, result_dict, limit):
    query_string = "SELECT gram, gram_value FROM frequency ORDER BY maximum DESC LIMIT {}".format(limit)
    iterate_cursor = connection.cursor()
    iterate_cursor.execute(query_string)
    index_dict = dict()
    for gram in range(settings.start_gram, settings.end_gram + 1):
        index_dict[gram] = 0
    for gram, gram_value in iterate_cursor:
        result_dict[gram][gram_value] = index_dict[gram]
        index_dict[gram] += 1


def update_by_dict(connection, gram_dict, file_type):
    cursor = connection.cursor()
    for gram_key, frequency in gram_dict.items():
        query_string = "INSERT OR IGNORE INTO frequency VALUES ({}, {}, {})".format(gram_key[0], gram_key[1], _zeros)
        connection.cursor().execute(query_string)

        query_string = "UPDATE frequency SET {} = {} + {} WHERE gram = {} AND gram_value = {}"\
            .format(file_type, file_type, frequency, gram_key[0], gram_key[1])
        cursor.execute(query_string)
    connection.commit()
