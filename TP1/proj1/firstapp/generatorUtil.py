divClass = {
        "staff": '1',
        "prole": '2',
        "serial": '3',
        "others": '4',
        'doctor': '21',
        'nurse': '22',
        'receptionist':'23',
        'manager': '24',
        'administrator': '25',
        'patient':'1',
        'invalid' : "",
    }


class GenerateToken:

    # cat1 = staff, prole, serial or others
    # cat2 = members of staff: doctor, nurse, receptionist etc
    # N.B - cat2 is invalid for a serial number
    # serial = serial number of the person
    # N.B -  serial input as a string, not number
    def __init__(self, cat1, cat2, serial):
        self.cat1 = cat1
        self.cat2 = cat2
        self.serial = serial
        self.string = divClass[cat1] + divClass[cat2] + self.serialNo()

    def serialNo(self):
        n = len(self.serial)
        length = 3
        if self.cat1 == "prole":
            length = length + 1
        elif self.cat1 == "serial":
            length = length + 2
        string2 = ""
        for i in range(length - n):
            string2 = string2 + "0"
        x = 1 + int(self.serial)
        return string2 + str(x)

    def returnId(self):
        return self.string


if __name__ == "__main__":
    x = GenerateToken("prole", "patient", "4").returnId()
    print(x)