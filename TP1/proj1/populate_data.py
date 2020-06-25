import random

import cx_Oracle
from faker import Faker

from firstapp import execution as ex
from datetime import date, timedelta, datetime

from firstapp.generatorUtil import GenerateToken


def populate_date():
    s_date = date(2020, 6, 20)
    e_date = date(2020, 12, 31)
    conn = ex.connect()
    cur = conn.cursor()

    delta = e_date - s_date

    days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    dayI = 0
    for i in range(delta.days + 1):
        day = s_date + timedelta(days=i)
        hol = False
        weknd = False
        if (dayI + i) % 7 == 6:
            weknd = True
        # print(str(day) + " " + days[(dayI + i) % 7])
        sql = ''' insert into HOSPITAL.CALENDER(DATE_ID, FULL_DATE, DAY_IN_WEEK, DAY_NAME, IS_HOLIDAY)
                 VALUES(:ID, :FULLDATE, :DIW, :DN, :IS_HOLI)'''
        try:
            cur.execute(sql, [i + 1, day, (dayI + i) % 7 + 1, days[(dayI + i) % 7], "No"])
            conn.commit()
        except cx_Oracle.Error as error:
            print("Error occured")
            print(error)


def populate_time_table():
    fhand = open("timetable.txt", "r")
    if fhand.mode == 'r':
        lines = fhand.readlines()
        for line in lines:
            line = line.rstrip()
            line = line.split()
            cat = ""
            for i in range(3, len(line)):
                cat = cat + line[i]
                if i != len(line)-1:
                    cat = cat + " "
            sql = '''insert into HOSPITAL.TIME_TABLE(TIME_ID, START_TIME, END_TIME, SHIFT_TITLE)
                 VALUES(:ID, :START_TIME, :END_TIME, :TITLE)'''
            conn = ex.connect()
            cur = conn.cursor()
            try:
                cur.execute(sql,[line[0],line[1],line[2],cat])
                conn.commit()
            except cx_Oracle.Error as error:
                print("Error occured")
                print(error)


def populate_doctor(N = 10):
    random.seed(0)
    Faker.seed(0)
    fake = Faker()

    specialization = ["Cardiology", "Neurology", "Orthopedics", "Physiotherapy",
                      "Dentistry", "Oncology", "Pediatrics", "Obstetrics and Gynocology",
                      "Gastroenterology and Hepatology", "Dermatology and Venereology",
                      "Medicine", "Ophthalmologists"]

    designation = ["Assistant Professor", "Professor", "Associate Professor", "Dr. Professor", "Consultant"]
    qualification = ["PhD,DPhil", "MPhil", "MM,MMed", "MSurg", "FCPS", "FRCPS"]
    conn = ex.connect()
    cur = conn.cursor()

    for i in range(N):
        id = int(GenerateToken("staff", "doctor", str(i)).returnId())
        fname = fake.first_name()
        lname = fake.last_name()
        email = fname+lname+"@gmail.com"
        phn = str(fake.msisdn())
        dob = fake.date_time(end_datetime=datetime(1992, 12, 31, 23, 59, 59))
        hire = fake.date_time()
        addr = fake.address()
        spec = specialization[random.randint(0,11)]
        status = "active"
        des = designation[random.randint(0,4)]
        qua = qualification[random.randint(0,5)] + ", MBBS"
        gender = "Male"
        wrap = [id, fname, lname, email, phn, hire, gender, spec, des, qua, status, addr, dob]

        sql = '''insert into HOSPITAL.DOCTORS(DOC_ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NUMBER, HIRE_DATE,
                 GENDER, SPECIALIZATION, DESIGNATION, QUALIFICATION, STATUS, ADDRESS, DATE_OF_BIRTH)
                 VALUES(:ID, :FNAME, :LNAME, :EMAIL, :PHN, :HIRE, :GEN, :SPEC, :DES, :QUA, :STAT, :ADDR, :DOB)'''
        try:
            cur.execute(sql, wrap)
            conn.commit()
        except cx_Oracle.Error as error:
            print("Error occured")
            print(error)


if __name__ == "__main__":
    populate_doctor(25)

