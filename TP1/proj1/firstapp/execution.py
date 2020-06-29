import cx_Oracle
from datetime import datetime
from firstapp import generatorUtil

patient_threshold = 30


def connect(user_n='hospital', pass_n='hospital', host='localhost', port='1521', service_n='ORCL'):
    dsn_tns = cx_Oracle.makedsn(host, port, service_name=service_n)
    conn = cx_Oracle.connect(user=user_n, password=pass_n, dsn=dsn_tns)

    return conn


def get_cursor():
    conn = connect()
    return [conn, conn.cursor()]


def exe_select_get_data(sql):
    _, cur = get_cursor()
    try:
        cur.execute(sql)
        return dictfetchall(cur)
    except cx_Oracle.Error as e:
        print("Error occur")
        print(e)


def getDoctorInfo():
    con = connect().cursor()
    con.execute("SELECT * from HOSPITAL.DOCTORS")
    out = ''
    # print(c)
    for row in con:
        out += str(row) + '\n '
    return out


def patientregister(datadict):
    conn, cur = get_cursor()

    sql = '''Select * from HOSPITAL.PATIENT 
             where EMAIL = ''' + "'" + datadict['email'] + "'"
    cur.execute(sql)
    cur.fetchall()
    if cur.rowcount > 0:
        return "duplicate"

    cur.execute('''SELECT MAX(PATIENT_ID) FROM HOSPITAL.PATIENT''')
    data = cur.fetchone()
    if cur.rowcount == 0:
        datadict['id'] = int(generatorUtil.GenerateToken("prole", "patient", "0").returnId())
    else:
        id_serial = data[0]
        print("serial =" + str(id_serial))
        datadict['id'] = id_serial + 1

    print(datadict)
    sql = (
        'insert into HOSPITAL.PATIENT(PATIENT_ID,FIRST_NAME,LAST_NAME,EMAIL,PHONE_NUM,GENDER,ADDRESS,DATE_OF_BIRTH, ID_STATUS)'
        'values(:id,:fname,:lname,:email,:phn,:gender,:address,:dob, :status)')

    try:
        cur.execute(sql, [datadict['id'], datadict['f_name'], datadict['l_name'], datadict['email'],
                          datadict['phn'], datadict['gender'],
                          datadict['address'], datadict['dob'], datadict['status']])
        conn.commit()
        print("successfully executed")
        return "successful"
    except cx_Oracle.Error as error:
        print("Error occured")
        print(error)
        return "unsuccessful"


def getpatientinfo():
    con = connect()
    cur = con.cursor()
    cur.execute("Select * from HOSPITAL.PATIENT order by PATIENT_ID")
    info_dict = dictfetchall(cur)
    return info_dict


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def getDocSelect(specialization):
    conn, cur = get_cursor()
    sql = '''select DOC_ID,(FIRST_NAME||' '||LAST_NAME) as DOC_NAME from HOSPITAL.DOCTORS
             where SPECIALIZATION =''' + "'" + specialization + "'"
    try:
        cur.execute(sql)
        return dictfetchall(cur)
    except cx_Oracle.Error as e:
        print(e)


def get_time_category():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute('''Select TIME_ID, SHIFT_TITLE from HOSPITAL.TIME_TABLE order by TIME_ID''')
        data = dictfetchall(cur)
        # print(data)
        return data
    except cx_Oracle.Error as error:
        print(error)


def get_doc_list_by_id(docId):
    _, cur = get_cursor()
    try:
        cur.execute('''Select (FIRST_NAME||' '||LAST_NAME) as NAME, DESIGNATION, SPECIALIZATION
                        from HOSPITAL.DOCTORS where DOC_ID = ''' + docId)
        data = dictfetchall(cur)
        # print(cur.description)
        return data
    except cx_Oracle.Error as error:
        print(error)


def get_doc_schedule(docId):
    _, cur = get_cursor()
    try:
        sql = '''SELECT S.SCHEDULE_ID, C.FULL_DATE, T.SHIFT_TITLE, T.START_TIME, T.END_TIME
                from DOCTORS D join SCHEDULE S
                on (D.DOC_ID = S.DOC_ID)
                join TIME_TABLE T
                on(S.SHIFT_ID = T.TIME_ID)
                join CALENDER C
                on(S.KEY_DATE = C.DATE_ID)
                where D.DOC_ID = ''' + str(docId) + '''order by S.SCHEDULE_ID'''

        cur.execute(sql)
        data = dictfetchall(cur)
        for entry in data:
            entry['FULL_DATE'] = str(entry['FULL_DATE']).split()[0]
        # print(data)
        return data
    except cx_Oracle.Error as error:
        print(error)


def save_doc_schedule(docId, date, time_id):
    conn, cur = get_cursor()
    try:
        cur.execute("SELECT DATE_ID FROM CALENDER where TRUNC(FULL_DATE) = TO_DATE('" + date + "', 'yy-MM-dd')")
        keydate = cur.fetchone()[0]
        # print(keydate)

        sql = ('select * from HOSPITAL.SCHEDULE '
               'where DOC_ID =' + "'" + docId + "'" +
               ' AND KEY_DATE=' + "'" + str(keydate) + "'" +
               ' AND SHIFT_ID=' + "'" + time_id + "'")

        cur.execute(sql)
        # print(cur.fetchone())
        if cur.rowcount > 0:
            return ["Duplicate"]
        cur.execute(''' Select Max(SCHEDULE_ID) from HOSPITAL.SCHEDULE''')
        newId = int(cur.fetchone()[0]) + 1
        # print(newId)

        sql = '''insert into HOSPITAL.SCHEDULE(SCHEDULE_ID, KEY_DATE, DOC_ID, SHIFT_ID)
                values(:id,:keyDate,:docID,:shiftId)'''
        cur.execute(sql, [newId, keydate, docId, time_id])
        conn.commit()
        return ["Done"]
    except cx_Oracle.Error as error:
        print(error)
        return ["Undone"]


def delete_schedule(schedule_id):
    conn, cur = get_cursor()
    sql = ('delete from HOSPITAL.SCHEDULE'
           ' where SCHEDULE_ID =' + "'" + schedule_id + "'")
    try:
        cur.execute(sql)
        conn.commit()
    except cx_Oracle.Error as e:
        print(e)


def get_pat_by_id(pat_id):
    _, cur = get_cursor()
    sql = '''select FIRST_NAME, LAST_NAME, EMAIL, GENDER, PHONE_NUM, ADDRESS, DATE_OF_BIRTH 
             from HOSPITAL.PATIENT
             where PATIENT_ID =' ''' + pat_id + "'"
    try:
        cur.execute(sql)
        data = dictfetchall(cur)
        print(data)
        if len(data) > 0:
            data[0]['DATE_OF_BIRTH'] = str(data[0]['DATE_OF_BIRTH']).split()[0]
        return data
    except cx_Oracle.Error as e:
        print(e)


def process_app_req_init(datadict):
    """
    initial appointment processing function that gives next possible dates and doctor info
    :param datadict: the dict containing patient appointment info after parsing
    :return: info_dict: has details, final_date_dict: all possible upcoming schedule dates of doctor
    """
    pat_id = datadict['pat_id']
    if len(pat_id) == 0:
        sql = ('''select PATIENT_ID from HOSPITAL.PATIENT
                 where FIRST_NAME = ''' + "'" + datadict['p_f_name'] + "'" +
               ''' AND EMAIL = ''' + "'" + datadict['p_email'] + "'")
        data = exe_select_get_data(sql)
        pat_id = data[0]['PATIENT_ID']

    info_dict = {
        'PATIENT ID': pat_id,
        'DOCTOR ID': datadict['doc_id'],
        'PROBLEM DESCRIPTION': datadict['prob_desc']
    }
    sql = '''select (FIRST_NAME||' '||LAST_NAME) as "DOCTOR NAME", SPECIALIZATION, 
             DESIGNATION, QUALIFICATION
             from HOSPITAL.DOCTORS
             where DOC_ID = ''' + datadict['doc_id']
    doc_info = exe_select_get_data(sql)[0]

    for key in doc_info.keys():
        info_dict[key] = str(doc_info[key])
    # print(info_dict)

    today = str(datetime.today()).split()[0]
    sql = '''select DATE_ID from calender
             where FULL_DATE = TO_DATE(''' + "'" + today + "','yyyy-mm-dd')"
    today = exe_select_get_data(sql)
    today = str(today[0]['DATE_ID'])
    # print(today)

    sql = ('''select S.KEY_DATE, COUNT(A.APP_DATE_KEY) as app_count
            from SCHEDULE S join APPOINTMENT A
            on(A.APP_DATE_KEY = S.KEY_DATE
            and A.DOCTOR_ID = S.DOC_ID
            and A.DOCTOR_ID = ''' + info_dict['DOCTOR ID'] +
           '''and A.APP_DATE_KEY >''' + today + ")" +
           '''GROUP BY S.KEY_DATE, A.APP_DATE_KEY''')

    app_data = exe_select_get_data(sql)
    app_dict = {}
    for date in app_data:
        app_dict[str(date["KEY_DATE"])] = date['APP_COUNT']
    # print(app_dict)

    sql = ('''select DISTINCT(S.KEY_DATE), C.FULL_DATE, T.TIME_ID, T.START_TIME, T.END_TIME
                from CALENDER C 
                join SCHEDULE S
                on(S.KEY_DATE = C.DATE_ID)
                join TIME_TABLE T
                on(S.SHIFT_ID = T.TIME_ID)
                where (S.SHIFT_ID = 6 or S.SHIFT_ID = 7) and
                S.KEY_DATE > ''' + today + " and " +
           "S.DOC_ID = " + info_dict['DOCTOR ID'] +
           " order by S.KEY_DATE asc")
    schedule_data = exe_select_get_data(sql)
    # print("schedule data")
    # print(schedule_data)

    for i in range(len(schedule_data)):
        schedule_data[i]['FULL_DATE'] = str(schedule_data[i]['FULL_DATE']).split()[0]

    final_date_dict = []
    if len(app_dict) > 0:
        for schedule in schedule_data:
            date_key = str(schedule['KEY_DATE'])
            if date_key in app_dict:
                if app_dict[date_key] < patient_threshold:
                    final_date_dict.append(schedule)
            else:
                final_date_dict.append(schedule)
    else:
        final_date_dict = schedule_data
    # print("Final Product")
    # print(final_date_dict)

    return info_dict, final_date_dict


def save_app(datadict):
    conn, cur = get_cursor()
    print(datadict)
    try:
        # fetch today's key_date
        today = str(datetime.today()).split()[0]
        sql = '''select DATE_ID from calender
                     where FULL_DATE = TO_DATE(''' + "'" + today + "','yyyy-mm-dd')"
        today = exe_select_get_data(sql)
        today = str(today[0]['DATE_ID'])

        # see if there are any duplicates
        sql = (''' select * from HOSPITAL.APPOINTMENT
                where PATIENT_ID = ''' + datadict['pat_id'] +
               " and DOCTOR_ID = " + datadict['doc_id'] +
               " and APP_DATE_KEY > " + today +
               " and STATUS = 'issued'")
        data = exe_select_get_data(sql)
        if len(data) > 0:
            return "duplicate"

        cur.execute("Select MAX(APP_SL_NO) from HOSPITAL.APPOINTMENT")
        app_id = int(cur.fetchone()[0]) + 1
        issue_date = datetime.now()
        status = "issued"

        lst = [app_id, int(datadict['pat_id']),
               int(datadict['doc_id']), int(datadict['date_key']),
               datadict['desc'], status, issue_date, datadict['time_id']]

        sql = '''insert into HOSPITAL.APPOINTMENT(APP_SL_NO, PATIENT_ID, DOCTOR_ID, 
                APP_DATE_KEY, PROBLEM_DESC, STATUS, ISSUE_DATE, TIME_ID) 
                values(:app_sl,:pat_id,:doc_id,:date_key,:des,:status, :i_date, :time_id)'''

        cur.execute(sql, lst)
        conn.commit()
        return "successful"
    except cx_Oracle.Error as e:
        print("Error Occured")
        print(e)
        return "unsuccessful"


if __name__ == "__main__":
    d = {
        "pat_id": "1210001",
        "p_f_name": "",
        "p_email": "",
        "doc_id": "121005",
        "app_date": "",
        "prob_desc": "pete betha",
    }
    process_app_req_init(d)
