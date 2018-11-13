import hashlib


class HashChecker:
    def __init__(self):
        self.current_hash_set = set()

    def duplicated(self, data):
        hash_value = hashlib.md5(data.encode("utf-8")).hexdigest()
        if hash_value in self.current_hash_set:
            return True
        else:
            self.current_hash_set.add(hash_value)
            return False
