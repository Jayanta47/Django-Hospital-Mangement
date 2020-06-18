from firstapp import execution as ex
from firstapp import generatorUtil
import cx_Oracle


class Patient:
    insert_sql = """ insert into HOSPITAL.PATIENT(PATIENT_ID,FIRST_NAME,LAST_NAME,EMAIL,PHONE_NUM,GENDER,ADDRESS,DATE_OF_BIRTH)
           values(:id,:fname,:lname,:email,:phn,:gender,:address,:dob) """

    def __init__(self, datadict):
        self.datadict = datadict
        self.patientid = ""

    def getBuiltId(self, cur):
        idnum = cur.execute("SELECT COUNT(*) FROM HOSPITAL.PATIENT").fetchone()[0]
        fun = generatorUtil.GenerateToken("prole", "patient", str(idnum))
        self.patientid = fun.returnId()

    def savetoDB(self):
        conn = ex.connect()
        cur = conn.cursor()
        self.getBuiltId(cur)
        #print(self.patientid)
        self.datadict['id'] = int(self.patientid)
        #print(self.datadict)
        try:
            cur.execute(self.insert_sql, [self.datadict['id'], self.datadict['fname'], self.datadict['lname'],
                                          self.datadict['email'], self.datadict['phn'], self.datadict['gender'],
                                          self.datadict['address'], self.datadict['dob']])
            #conn.commit()
        except cx_Oracle.Error as error:
            print("Error occured")
            print(error)
#   def extractDataList(self):



