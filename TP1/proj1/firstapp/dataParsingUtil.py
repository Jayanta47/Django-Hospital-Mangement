patientCols = ['fname', 'lname', 'email', 'phn', 'gender', 'address', 'dob']


def patientRegisterParse(post):
    datadict = {}
    for value in patientCols:
        datadict[value] = post.get(value)
    return datadict
