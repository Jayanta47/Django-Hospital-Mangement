from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from . import execution

# Create your views here.


@api_view(['GET'])
def options(request):
    api_urls = {
        'login': '/login/',
        'logout': '/logout'
    }
    return Response(api_urls)


@api_view(['POST'])
def login(request):
    body = request.body.decode('utf-8')
    credentials = json.loads(body)
    response = execution.authenticateUser(credentials)
    #print(response)
    return Response(response)


@api_view(['POST'])
def getUserInfo(request):
    body = request.body.decode('utf-8')
    userInfo = json.loads(body)
    #print(userInfo)
    response = execution.getUserData(userInfo)
    # #print(response)

    return Response(response)


@api_view(['GET', 'PUT'])
def getReceptionistAppointments(request):
    if(request.method == "PUT"):
        body = request.body.decode('utf-8')
        appointmentInfo = json.loads(body)
        #print(appointmentInfo)
        appointments = execution.getAppointments(appointmentInfo)
        return Response(appointments)

    else:
        appointments = execution.getAppointments()
        return Response(appointments)


@api_view(['POST'])
def getDoctorAppointments(request):
    body = request.body.decode('utf-8')
    docId = json.loads(body)
    #print(docId)
    response = execution.getDocAppointments(docId['DOC_ID'])
    return Response(response)


@api_view(['GET'])
def getDoctorTests(request):
    response = execution.getDoctorTests()
    return Response(response)


@api_view(['GET'])
def getDoctorSurgery(request):
    response = execution.getDoctorSurgery()
    return Response(response)


@api_view(['POST'])
def docDiagnosis(request):
    body = request.body.decode('utf-8')
    diagnosis = json.loads(body)
    #print(diagnosis)

    app_sl_no = None
    testId = None
    surgeryId = None
    surgeryDesc = None
    surgeryResult = None
    medicine = None

    if 'APP_SL_NO' in diagnosis:  # check if a key exists in a dictionary
        app_sl_no = diagnosis['APP_SL_NO']
    if 'TEST_ID' in diagnosis:
        testId = diagnosis['TEST_ID']
    if 'SURGERY_ID' in diagnosis:
        surgeryId = diagnosis['SURGERY_ID']
    if 'SURGERY_DESCRIPTION' in diagnosis:
        surgeryDesc = diagnosis['SURGERY_DESCRIPTION']
    if 'MEDICINE' in diagnosis:
        medicine = diagnosis['MEDICINE']
    if 'SURGERY_RESULT' in diagnosis:
        surgeryResult = diagnosis['SURGERY_RESULT']

    print(f"{app_sl_no}, {testId}, {surgeryId},{surgeryDesc}, {medicine}, {surgeryResult}")
    response = execution.docDiagnosis(app_sl_no, testId, surgeryId,surgeryDesc, surgeryResult, medicine)

    #response = {'success': True}

    return Response(response)


@api_view(['POST'])
def getServiceResults(request):
    body = request.body.decode('utf-8')
    serviceInfo = json.loads(body)

    #print(serviceInfo)

    app_sl_no = serviceInfo["APP_SL_NO"]

    response = execution.getServiceResults(app_sl_no)

    return Response(response)


@api_view(['POST'])
def showUpcomingSurgeries(request):
    body = request.body.decode('utf-8')
    docId = json.loads(body)
    #print(docId)
    response = execution.showSurgeries(docId['DOC_ID'])
    return Response(response)


@api_view(['GET'])
def technicianTests(request):
    response = execution.technicianTests()
    return Response(response)

@api_view(['POST'])
def technicianTestResult(request):
    body = request.body.decode('utf-8')
    testResult = json.loads(body)

    #response = execution.technicianTestResult(testResult)
    print(testResult)

    response = {'Success': True}

    return Response(response)