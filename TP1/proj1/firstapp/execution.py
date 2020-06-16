import cx_Oracle


def connect(user_n='hospital', pass_n='hospital' ,host='localhost', port='1521', service_n='ORCL'):
    dsn_tns = cx_Oracle.makedsn(host, port, service_name=service_n)
    conn = cx_Oracle.connect(user=user_n, password=pass_n, dsn=dsn_tns)

    return conn


def getDoctorInfo():
    con = connect().cursor()
    con.execute("SELECT * from HOSPITAL.DOCTORS")
    out = ''
    #print(c)
    for row in con:
        out +=str(row) + ' \n '
    return out


def patientregister(datadict):
    conn = connect()
    cur = conn.cursor()

    idq = cur.execute("SELECT COUNT(*) FROM HOSPITAL.PATIENT")
    num = idq.fetchone()[0]

    num = num + 1
    datadict['id'] = num
    print("id = "+ str(num))
    if datadict['gender'] == '1':
        datadict['gender'] = 'Male'
    else:
        datadict['gender'] = 'Female'

    sql = ('insert into HOSPITAL.PATIENT(PATIENT_ID,FIRST_NAME,LAST_NAME,EMAIL,PHONE_NUM,GENDER,ADDRESS,DATE_OF_BIRTH)'
           'values(:id,:fname,:lname,:email,:phn,:gender,:address,:dob)')

    id = num
    fname = datadict['fname']
    lname = datadict['lname']
    email = datadict['email']
    phn = datadict['phn']
    gender = datadict['gender']
    address = datadict['address']
    dob = datadict['dob']

    # the data should be ordered inorder to be inserted, the data in a dict is not ordered
    try:
        #con.execute(sql, [id,fname,lname,email,phn,gender,address,dob])
        cur.execute(sql, [datadict['id'],datadict['fname'],datadict['lname'],datadict['email'],datadict['phn'],datadict['gender'],
                 datadict['address'],datadict['dob']])
        conn.commit()
        print("successfully executed")
    except cx_Oracle.Error as error:
        print("Error occured")
        print(error)

    obj = cur.execute("SELECT * from HOSPITAL.Patient")
    out = ''
    # print(c)
    for row in obj:
        out += str(row) + ' \n '

    print(out)
    # con.execute("""
    #             insert into PATIENT (PATIENT_ID,FIRST_NAME,LAST_NAME,EMAIL,PHONE_NUM,GENDER,ADDRESS,DATE_OF_BIRTH)
    #             values (:id,:fname,:lname,:email,:phn,:gender,:address,:dob)
    #             """,  datadict['id'],datadict['fname'],datadict['lname'],datadict['email'],datadict['phn'],datadict['gender'],
    #             datadict['address'],datadict['dob'])
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



