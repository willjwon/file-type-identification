import unittest


class IOManager:
    @staticmethod
    def ask_string(message):
        reply = str(input(message))
        print()
        return reply

    @staticmethod
    def ask_int(message):
        end_flag = False
        reply = None
        while not end_flag:
            try:
                reply = int(input(message))
                end_flag = True
            except ValueError:
                print("The input value is not integer! Please try again.")
            print()
        return reply


class IOManagerTest(unittest.TestCase):
    def setUp(self):
        self.ioManager = IOManager()

    def test_askString(self):
        self.assertEqual(self.ioManager.ask_string("type 'hello'"), "hello")

    def test_askInt(self):
        self.assertEqual(self.ioManager.ask_int("type '3'"), 3)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
