from datetime import datetime

patientCols = ['f_name', 'l_name', 'email', 'phn', 'gender', 'address', 'dob', 'status']
app_cols = ["pat_id", "p_f_name", "p_email", "doc_id", "prob_desc"]
app_cols_final = ["pat_id", "doc_id", "desc", "date_key", "time_id"]

def patientRegisterParse(post):
    datadict = {}
    for value in patientCols:
        datadict[value] = post.get(value)
    datadict['dob'] = datetime.fromisoformat(datadict['dob'] + "T00:00:00")
    return datadict


def app_register_parse(post):
    datadict = {}
    for value in app_cols:
        datadict[value] = str(post.get(value))
    return datadict


def app_reg_final_parse(post):
    datadict = {}
    for value in app_cols_final:
        datadict[value] = post.get(value)
    return datadict
