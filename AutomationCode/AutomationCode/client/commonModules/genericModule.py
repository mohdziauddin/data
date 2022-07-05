import random
import string


class genericModule:
    def __init__(self):
        pass

    def generateRandomNumber(self):
        number = random.randint(100000, 999999)
        return number

    def generateString(self, length):
        stringElements = ""
        for i in range(length):
            stringElements += string.ascii_uppercase + string.ascii_lowercase + string.digits
        result = ''.join(random.sample(stringElements, length))
        return result


# cl = genericModule()
# print(cl.generateString(127000))
