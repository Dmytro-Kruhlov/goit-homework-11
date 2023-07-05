class Test:
    count = 0
    def __new__(cls):
        instance = super().__new__(cls)
        cls.count += 1
        print(f"Hello< {cls.count}")
        return instance
    def __init__(self):
        print("You")


a = Test()
b = Test()
c = Test()
a