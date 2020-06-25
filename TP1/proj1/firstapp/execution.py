import cx_Oracle
from firstapp import generatorUtil


def connect(user_n='hospital', pass_n='hospital', host='localhost', port='1521', service_n='ORCL'):
    dsn_tns = cx_Oracle.makedsn(host, port, service_name=service_n)
    conn = cx_Oracle.connect(user=user_n, password=pass_n, dsn=dsn_tns)

    return conn


def get_cursor():
    conn = connect()
    return [conn, conn.cursor()]


def getDoctorInfo():
    con = connect().cursor()
    con.execute("SELECT * from HOSPITAL.DOCTORS")
    out = ''
    #print(c)
    for row in con:
        out +=str(row) + '\n '
    return out


def patientregister(datadict):
    conn = connect()
    cur = conn.cursor()

    idq = cur.execute("SELECT COUNT(*) FROM HOSPITAL.PATIENT").fetchone()[0]
    datadict['id'] = int(generatorUtil.GenerateToken("prole", "patient", str(idq)).returnId())

    sql = ('insert into HOSPITAL.PATIENT(PATIENT_ID,FIRST_NAME,LAST_NAME,EMAIL,PHONE_NUM,GENDER,ADDRESS,DATE_OF_BIRTH)'
           'values(:id,:fname,:lname,:email,:phn,:gender,:address,:dob)')

    try:
        cur.execute(sql, [datadict['id'],datadict['fname'],datadict['lname'],datadict['email'],
                          datadict['phn'],datadict['gender'],
                          datadict['address'],datadict['dob']])
        conn.commit()
        print("successfully executed")
    except cx_Oracle.Error as error:
        print("Error occured")
        print(error)

    return


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
    con = connect()
    cur = con.cursor()
    specialization = "'" + specialization + "'"
    cur.execute("select (FIRST_NAME||' '||LAST_NAME) as FULL_NAME from HOSPITAL.DOCTORS where SPECIALIZATION = "
                + specialization)
    infodict = dictfetchall(cur)
    return infodict


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
        newId = int(cur.fetchone()[0])+1
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


if __name__ == "__main__":
    get_doc_schedule("121003")
