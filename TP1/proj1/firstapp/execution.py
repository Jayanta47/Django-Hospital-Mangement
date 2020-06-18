import cx_Oracle
from firstapp import generatorUtil


def connect(user_n='hospital', pass_n='hospital', host='localhost', port='1521', service_n='ORCL'):
    dsn_tns = cx_Oracle.makedsn(host, port, service_name=service_n)
    conn = cx_Oracle.connect(user=user_n, password=pass_n, dsn=dsn_tns)

    return conn


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
    specialization = "'"+specialization+"'"
    cur.execute("select (FIRST_NAME||' '||LAST_NAME) as FULL_NAME from HOSPITAL.DOCTORS where SPECIALIZATION = " + specialization)
    infodict = dictfetchall(cur)
    return infodict
