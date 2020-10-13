import cx_Oracle
import hashlib
from datetime import datetime


def connect(user_n='hospital', pass_n='hospital', host='localhost', port='1521', service_n='ORCL'):
    dsn_tns = cx_Oracle.makedsn(host, port, service_name=service_n)
    conn = cx_Oracle.connect(user=user_n, password=pass_n, dsn=dsn_tns)

    return conn


def passwordHash(password):
    result = hashlib.md5(password.encode())
    return result.hexdigest()


def is_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def executeQuery(query):
    with connect().cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def executeUpdateQuery(query):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()


def authenticateUser(creds):
    # print(creds)
    # print(creds['userId'])
    sql = "SELECT * FROM HOSPITAL.CREDENTIALS WHERE ID = " + creds['userId']
    result = executeQuery(sql)
    # print(result)

    if(len(result) == 0):
        return {
            'success': False
        }

    elif(result[0][1] == passwordHash(creds['password'])):
        token = 'loggedInUser'
        typeOfUSer = result[0][2]
        if(typeOfUSer == "EMPLOYEE"):
            typeOfUSer = executeQuery(
                f"SELECT EMPLOYEE_TYPE FROM HOSPITAL.EMPLOYEE WHERE EMP_ID = {creds['userId']}")[0][0]
        return {
            'success': True,
            'token': token,
            'type': typeOfUSer
        }
    else:
        return {
            'success': False
        }


def getUserData(userInfo):
    col_names_query = ""
    if(userInfo['type'] == 'DOCTORS' or userInfo['type'] == 'PATIENT'):
        col_names_query = f"select COLUMN_NAME from ALL_TAB_COLUMNS where TABLE_NAME='{userInfo['type']}'"
    else:
        col_names_query = "select COLUMN_NAME from ALL_TAB_COLUMNS where TABLE_NAME='EMPLOYEE'"
    col_names = executeQuery(col_names_query)

    sql = ''
    if(userInfo['type'] == 'DOCTORS'):
        sql = f"SELECT * FROM HOSPITAL.{userInfo['type']} WHERE DOC_ID = {userInfo['userId']}"
    elif(userInfo['type'] == 'PATIENT'):
        sql = f"SELECT * FROM HOSPITAL.{userInfo['type']} WHERE PATIENT_ID = {userInfo['userId']}"
    else:
        sql = f"SELECT * FROM HOSPITAL.EMPLOYEE WHERE EMP_ID = {userInfo['userId']}"

    userData = executeQuery(sql)

    user = {}
    length = len(col_names)

    for i in range(length):
        if(isinstance(userData[0][i], datetime)):
            # print('ulala')
            date = userData[0][i].strftime('%d-%b-%y')
            user.update({col_names[length-i-1][0]: date})

        else:
            user.update({col_names[length-i-1][0]: userData[0][i]})

    return user


def getAppointments(app_sl_no=""):
    appointments = []

    col_names_query = "select COLUMN_NAME from ALL_TAB_COLUMNS where TABLE_NAME='APPOINTMENT'"
    col_names = executeQuery(col_names_query)

    if(app_sl_no != ""):
        query = f"UPDATE HOSPITAL.APPOINTMENT SET STATUS = 'accepted' WHERE APP_SL_NO = {app_sl_no['APP_SL_NO']}"
        executeUpdateQuery(query)
        patientId = executeQuery(
            f"SELECT PATIENT_ID FROM HOSPITAL.APPOINTMENT WHERE APP_SL_NO = {app_sl_no['APP_SL_NO']}")[0][0]
        patientInfo = executeQuery(
            f"SELECT * FROM HOSPITAL.PATIENT WHERE PATIENT_ID = {patientId}")[0]
        # print(patientInfo[9])
        if(patientInfo[9] == "TP"):
            executeUpdateQuery(
                f"UPDATE HOSPITAL.PATIENT SET ID_STATUS = 'PM' WHERE PATIENT_ID = {patientId}")

    sql = "SELECT * FROM HOSPITAL.APPOINTMENT WHERE STATUS = 'issued'"
    allAppointments = executeQuery(sql)

    length = len(col_names)
    singleData = {}

    for individual in allAppointments:
        for i in range(len(individual)):
            if(isinstance(individual[i], datetime)):
                date = individual[i].strftime('%d-%b-%y')
                singleData.update({col_names[length-i-1][0]: date})

            else:
                singleData.update({col_names[length-i-1][0]: individual[i]})

        appointments.append(singleData.copy())
        singleData.clear()

    # print(appointments)

    return appointments


def getDocAppointments(docId):
    appointments = []

    col_names_query = "select COLUMN_NAME from ALL_TAB_COLUMNS where TABLE_NAME='APPOINTMENT'"
    col_names = executeQuery(col_names_query)

    allAppointments = executeQuery(
        f"SELECT * FROM HOSPITAL.APPOINTMENT WHERE DOCTOR_ID = {docId} AND STATUS = 'accepted'")
    #print(allAppointments)

    length = len(col_names)
    singleData = {}

    for individual in allAppointments:
        for i in range(len(individual)):
            if(isinstance(individual[i], datetime)):
                date = individual[i].strftime('%d-%b-%y')
                singleData.update({col_names[length-i-1][0]: date})

            else:
                singleData.update({col_names[length-i-1][0]: individual[i]})

        appointments.append(singleData.copy())
        singleData.clear()

    # print(appointments)

    #print(appointments)

    return appointments


def getDoctorTests():
    allTests = executeQuery(f"SELECT * FROM HOSPITAL.TEST")
    response = []
    for test in allTests:
        response.append(
            {"TEST_ID": test[0], "NAME": test[1], "DESCRIPTION": test[2], "COST": test[3]})
    # print(response)
    return response


def getDoctorSurgery():
    allSurgery = executeQuery(f"SELECT * FROM HOSPITAL.SURGERY")
    response = []
    for surgery in allSurgery:
        response.append({"SURGERY_ID": surgery[0], "NAME": surgery[1],
                         "DESCRIPTION": surgery[2], "COST": surgery[3], "DEPARTMENT": surgery[4]})

    return response


def docDiagnosis(app_sl_no, testId, surgeryId, surgeryDesc, surgeryResult, medicine):
    response = {}
    if(testId != None):
        allTestId = testId.strip().split('-')

        for ID in allTestId:
            query = f"INSERT INTO HOSPITAL.TEST_RESULTS(TEST_ID, COMPLETED) VALUES({int(ID)}, 'F')"
            executeUpdateQuery(query)
            testResultId = executeQuery(
                f"SELECT MAX(TEST_RESULT_ID) FROM HOSPITAL.TEST_RESULTS")
            testResultId = testResultId[0][0]

            diagnosisResult = executeQuery(
                f"SELECT SERVICE_RESULTS FROM HOSPITAL.DIAGNOSIS WHERE APP_SL_NO = {int(app_sl_no)}")
            # print(diagnosisResult[0])

            if(len(diagnosisResult) == 0):
                query = f"INSERT INTO HOSPITAL.DIAGNOSIS(APP_SL_NO, SERVICE_RESULTS) VALUES({int(app_sl_no)}, {str(testResultId)})"

                executeUpdateQuery(query)
                #print('1st if')

            else:
                query = f"UPDATE HOSPITAL.DIAGNOSIS SET SERVICE_RESULTS = '{str(diagnosisResult[0][0])}-{str(testResultId)}' WHERE APP_SL_NO = {int(app_sl_no)}"

                executeUpdateQuery(query)
                #print('2nd if')
        
        response = {'success': True}

    if(medicine != None):
        diagnosisResult = executeQuery(
            f"SELECT * FROM HOSPITAL.DIAGNOSIS WHERE APP_SL_NO = {int(app_sl_no)}")
        if(len(diagnosisResult) == 0):
            query = f"INSERT INTO HOSPITAL.DIAGNOSIS(APP_SL_NO,MEDICINE) VALUES({int(app_sl_no)}, '{str(medicine)}')"
            executeUpdateQuery(query)
            #print('3rd if')

        else:
            query = ""
            if(diagnosisResult[0][2] != None):
                query = f"UPDATE HOSPITAL.DIAGNOSIS SET MEDICINE = '{str(diagnosisResult[0][2])}-{str(medicine)}' WHERE APP_SL_NO = {int(app_sl_no)}"
            else:
                query = f"UPDATE HOSPITAL.DIAGNOSIS SET MEDICINE = '{str(medicine)}' WHERE APP_SL_NO = {int(app_sl_no)}"

            executeUpdateQuery(query)
            #print('4th if')
        
        response = {'success': True}

    if(surgeryId != None):
        allSurgeryId = surgeryId.strip().split('-')

        for ID in allSurgeryId:
            query = f"INSERT INTO HOSPITAL.SURGERY_RESULTS(SURGERY_ID, COMPLETED) VALUES({int(ID)}, 'F')"
            executeUpdateQuery(query)

            surgeryResultId = executeQuery(f"SELECT MAX(SURGERY_RESULT_ID) FROM HOSPITAL.SURGERY_RESULTS")
            surgeryResultId = surgeryResultId[0][0]

            diagnosisResult = executeQuery(f"SELECT SERVICE_RESULTS FROM HOSPITAL.DIAGNOSIS WHERE APP_SL_NO = {int(app_sl_no)}")
            #print(diagnosisResult)

            if(len(diagnosisResult) == 0):
                query = f"INSERT INTO HOSPITAL.DIAGNOSIS(APP_SL_NO, SERVICE_RESULTS) VALUES({int(app_sl_no)}, {str(surgeryResultId)})"

                executeUpdateQuery(query)
                #print('5th if')

            else:
                query = f"UPDATE HOSPITAL.DIAGNOSIS SET SERVICE_RESULTS = '{str(diagnosisResult[0][0])}-{str(surgeryResultId)}' WHERE APP_SL_NO = {int(app_sl_no)}"

                executeUpdateQuery(query)
                #print('6th if')

        response =  {'success': True}

    if(surgeryDesc != None):
        #print(surgeryDesc)
        query = f"INSERT INTO HOSPITAL.SURGERY_RESULTS(DESCRIPTION, COMPLETED) VALUES('{surgeryDesc}', 'F')"
        executeUpdateQuery(query)

        surgeryResultId = executeQuery(f"SELECT MAX(SURGERY_RESULT_ID) FROM HOSPITAL.SURGERY_RESULTS")
        surgeryResultId = surgeryResultId[0][0]

        diagnosisResult = executeQuery(f"SELECT SERVICE_RESULTS FROM HOSPITAL.DIAGNOSIS WHERE APP_SL_NO = {int(app_sl_no)}")
        #print(diagnosisResult)

        if(len(diagnosisResult) == 0):
            query = f"INSERT INTO HOSPITAL.DIAGNOSIS(APP_SL_NO, SERVICE_RESULTS) VALUES({int(app_sl_no)}, {str(surgeryResultId)})"

            executeUpdateQuery(query)
            #print('7th if')

        else:
            query = f"UPDATE HOSPITAL.DIAGNOSIS SET SERVICE_RESULTS = '{str(diagnosisResult[0][0])}-{str(surgeryResultId)}' WHERE APP_SL_NO = {int(app_sl_no)}"

            executeUpdateQuery(query)
            #print('8th if')
        response = {'success': True}
        

    if(surgeryResult != None):
        #print(surgeryResult)

        if 'STATUS' in surgeryResult:
            if 'MEDIA' in surgeryResult:
                #print('9th if')
                query = f"UPDATE HOSPITAL.SURGERY_RESULTS SET STATUS = '{surgeryResult['STATUS']}', MEDIA= '{surgeryResult['MEDIA']}' , COMPLETED = 'T'  WHERE SURGERY_RESULT_ID = {surgeryResult['SURGERY_RESULT_ID']}"
                #print(query)
                executeUpdateQuery(query)

                response = showSurgeries(surgeryResult['DOC_ID'])
            else:
                # print('10th if')
                query = f"UPDATE HOSPITAL.SURGERY_RESULTS SET STATUS = '{surgeryResult['STATUS']}', COMPLETED = 'T' WHERE SURGERY_RESULT_ID = {surgeryResult['SURGERY_RESULT_ID']}"
                #print(query)
                executeUpdateQuery(query)
                response = showSurgeries(surgeryResult['DOC_ID'])

        # if 'MEDIA' in surgeryResult:
        #     #print('9th if')
        #     query = f"UPDATE HOSPITAL.SURGERY_RESULTS SET STATUS = '{surgeryResult['STATUS']}', MEDIA= '{surgeryResult['MEDIA']}' , COMPLETED = 'T'  WHERE SURGERY_RESULT_ID = {surgeryResult['SURGERY_RESULT_ID']}"
        #     #print(query)
        #     executeUpdateQuery(query)
        # else:
        #     # print('10th if')
        #     query = f"UPDATE HOSPITAL.SURGERY_RESULTS SET STATUS = '{surgeryResult['STATUS']}', COMPLETED = 'T' WHERE SURGERY_RESULT_ID = {surgeryResult['SURGERY_RESULT_ID']}"
        #     #print(query)
        #     executeUpdateQuery(query)
        
    return response


def getServiceResults(app_sl_no):
    query = f"SELECT SERVICE_RESULTS FROM HOSPITAL.DIAGNOSIS WHERE APP_SL_NO = {app_sl_no}"
    nServices = executeQuery(query)
    nServices = nServices[0][0]

    services = nServices.strip().split('-')

    response = []

    for serviceId in services:
        if(serviceId[0:3] == "501"):
            singleResult = executeQuery(
                f"SELECT * FROM HOSPITAL.TEST_RESULTS WHERE TEST_RESULT_ID = {serviceId}")
            testName = executeQuery(
                f"SELECT NAME FROM HOSPITAL.TEST WHERE TEST_ID = {singleResult[0][1]}")

            # print(singleResult)

            if(singleResult[0][5] == "T"):
                # print("ulala")
                response.append({'TYPE': 'TEST', 'NAME': testName[0][0], "RESULT": singleResult[0][4],
                                 "MEDIA": singleResult[0][2], "DATE": singleResult[0][3].strftime('%d-%b-%y, %H:%M:%S')})
            elif(singleResult[0][5] == "F"):
                # print("ulala2")
                response.append(
                    {'TYPE': 'TEST', 'NAME': testName[0][0], "RESULT": "pending"})

        if(serviceId[0:3] == "601"):
            singleResult = executeQuery(
                f"SELECT * FROM HOSPITAL.SURGERY_RESULTS WHERE SURGERY_RESULT_ID = {serviceId}")
            #surgeryName = executeQuery(f"SELECT NAME FROM HOSPITAL.SURGERY WHERE SURGERY_ID = {singleResult[0][1]}")

            # print(singleResult)

            if(singleResult[0][6] == "T"):
                print("ulala3")
                if(singleResult[0][1] != None):
                    surgeryDesc = executeQuery(
                        f"SELECT * FROM SURGERY WHERE SURGERY_ID = {singleResult[0][1]}")
                    surgeryName = surgeryDesc[0][1]

                    response.append({'TYPE': 'SURGERY', "SURGERY_RESULT_ID": singleResult[0][0], "DESCRIPTION": surgeryName, "STATUS": singleResult[
                                    0][3], "MEDIA": singleResult[0][4], "DATE": singleResult[0][5].strftime('%d-%b-%y, %H:%M:%S')})

                else:
                    response.append({'TYPE': 'SURGERY', "SURGERY_RESULT_ID": singleResult[0][0], "DESCRIPTION": singleResult[0][
                                    2], "STATUS": singleResult[0][3], "MEDIA": singleResult[0][4], "DATE": singleResult[0][5].strftime('%d-%b-%y, %H:%M:%S')})

            elif(singleResult[0][6] == "F"):
                #print("ulala4")
                if(singleResult[0][1] != None):
                    surgeryDesc = executeQuery(
                        f"SELECT * FROM SURGERY WHERE SURGERY_ID = {singleResult[0][1]}")
                    surgeryName = surgeryDesc[0][1]

                    response.append(
                        {'TYPE': 'SURGERY', "SURGERY_RESULT_ID": singleResult[0][0], "DESCRIPTION": surgeryName, "STATUS": "pending"})

                else:
                    response.append(
                        {'TYPE': 'SURGERY', "SURGERY_RESULT_ID": singleResult[0][0], "DESCRIPTION": singleResult[0][2],  "STATUS": "pending"})

    return response


def showSurgeries(docId):
    query = f"SELECT APP_SL_NO FROM HOSPITAL.APPOINTMENT WHERE DOCTOR_ID = {docId} AND STATUS = 'accepted'"

    all_app_sl_no = executeQuery(query)

    # print(all_app_sl_no)

    response = []

    for app_sl_no in all_app_sl_no:
        # print(app_sl_no[0])
        query = f"SELECT SERVICE_RESULTS FROM HOSPITAL.DIAGNOSIS WHERE APP_SL_NO = {app_sl_no[0]}"
        service_results = executeQuery(query)
        # print(service_results)
        if(len(service_results) != 0):
            if(service_results[0][0] != None):
                services = service_results[0][0].strip().split('-')
                # print(services)

                for service in services:
                    if(service[0:3] == "601"):
                        # print("ulala")
                        query = f"SELECT * FROM HOSPITAL.SURGERY_RESULTS WHERE SURGERY_RESULT_ID = {service} AND COMPLETED = 'F' "
                        # print(query)
                        surgeryDetails = executeQuery(query)
                        # print(surgeryDetails)

                        if(len(surgeryDetails) != 0):
                            if(surgeryDetails[0][1] != None):
                                query = f"SELECT NAME FROM HOSPITAL.SURGERY WHERE SURGERY_ID = {surgeryDetails[0][1]}"
                                surgeryName = executeQuery(query)[0][0]
                                # print(surgeryName)

                                response.append(
                                    {"SURGERY_RESULT_ID": surgeryDetails[0][0], "DESCRIPTION": surgeryName})

                            else:
                                response.append(
                                    {"SURGERY_RESULT_ID": surgeryDetails[0][0], "DESCRIPTION": surgeryDetails[0][2]})

    #print(response)

    return response


def technicianTests():
    query = f"SELECT * FROM HOSPITAL.TEST_RESULTS WHERE COMPLETED = 'F'"
    allTests = executeQuery(query)

    response = []

    for test in allTests:
        query = f"SELECT NAME FROM HOSPITAL.TEST WHERE TEST_ID = {test[1]}"
        testName = executeQuery(query)
        testName = testName[0][0]

        response.append({"TEST_RESULT_ID": test[0], "TEST_ID": test[1], "TEST_NAME": testName})

    return response

def technicianTestResult(testResult):
    testResultId = testResult["TEST_RESULT_ID"]
    result = None
    media = None

    if "MEDIA" in testResult:
        media = testResult["MEDIA"]
    if "RESULT" in testResult:
        result = testResult["RESULT"]

    query = ""
    if media == None:
        query = f"UPDATE HOSPITAL.TEST_RESULTS SET RESULT = '{result}', COMPLETED = 'T' WHERE TEST_RESULT_ID = {testResultId}"
    
    else:
        query = f"UPDATE HOSPITAL.TEST_RESULTS SET RESULT = '{result}', MEDIA = '{media}' ,COMPLETED = 'T' WHERE TEST_RESULT_ID = {testResultId}"
    
    executeUpdateQuery(query)

    return {"SUCCESS": True}