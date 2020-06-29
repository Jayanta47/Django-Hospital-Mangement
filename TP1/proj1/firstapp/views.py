from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.

from firstapp import execution as ex
# from firstapp import dataModel as dm
from firstapp import dataParsingUtil as parse


def index(request):
    return render(request, 'firstapp/index.html')


def index2(request):
    c = ex.connect('hospital', 'hospital')
    str = ex.getDoctorInfo(c)
    print(str)
    c.close()
    return HttpResponse(str, content_type="text/plain")


def frontpage(request):
    return render(request, 'firstapp/frontpage.html')


def appointmentpage(request):
    if request.method == 'POST':
        print(request.POST.get('fname'))
        for key,value in request.POST.items():
            print(f'key: {key}')
            print(f'value : {value}')

    return render(request, 'firstapp/appointment.html')


def register_page(request):
    if request.method == 'POST':
        ex.patientregister(parse.patientRegisterParse(request.POST))
    return render(request, 'firstapp/register.html')

# def registerpage(request):
#     if request.method == 'POST':
#         listA = dict(request.POST).items()
#         print(listA)
#         listB = {}
#         for key,value in listA:
#             listB[str(key)] = request.POST.get(str(key))
#
#         fun = dm.Patient(listB)
#         fun.savetoDB()
#     return render(request, 'firstapp/register.html')


def employeepage(request):
    employee = [
        {'name': "Tokyo", 'age': 28, 'ntl' : "spanish"},
        {'name': "Madrid", 'age': 31, 'ntl': "spanish"},
        {'name': "Rio", 'age': 25, 'ntl': "Brazilian"},
        {'name': "Denver", 'age': 18, 'ntl': "American"}
    ]
    return render(request, 'firstapp/employees.html', {'employees': employee})


def patientpage(request):
    patient_info = ex.getpatientinfo()
    #print(patient_info)
    return render(request, 'firstapp/patients.html', {'patients': patient_info})


def loadcities(request):
    id = request.GET.get('country')
    cities = []
    if id == 'Bangladesh':
        cities = ['Dhaka', 'Khulna', 'Chittagong']
    elif id == 'India':
        cities = ['Kolkata', 'New Delhi', 'Ahmedabad', 'Pune']
    return render(request, 'firstapp/dropdown_list.html', {'cities': cities})


def testpage(request):
    return render(request, 'firstapp/test.html')


def loadDocSelect(request):
    specialization = request.GET.get('dept_name')
    data = ex.getDocSelect(specialization)
    return HttpResponse(json.dumps(data))


def schedule(request):
    time_lst = ex.get_time_category()
    return render(request, 'firstapp/scheduleTable.html', {'time_slot': time_lst})


def doc_data(request):
    docId = request.GET.get('docId', None)
    doc_lst = ex.get_doc_list_by_id(docId)
    return HttpResponse(json.dumps(doc_lst))


def doc_schedule(request):
    docId = request.GET.get('docId', None)
    doc_sch_lst = ex.get_doc_schedule(docId)
    return HttpResponse(json.dumps(doc_sch_lst))


def doc_save_schedule(request):
    docId = request.GET.get('docId', None)
    date = request.GET.get('date', None)
    time_slot = request.GET.get('time_slot', None)
    msg = ex.save_doc_schedule(docId, date, time_slot)
    return HttpResponse(json.dumps(msg))


def doc_delete_schedule(request):
    del_id_list = request.GET.get('list', None)
    del_id_list = json.loads(del_id_list)
    for id in del_id_list:
        ex.delete_schedule(id)
    return HttpResponse("")


def pat_data(request):
    pat_id = request.GET.get('pat_id')
    pat_info = ex.get_pat_by_id(pat_id)
    return HttpResponse(json.dumps(pat_info))


def patient_register(request):
    datadict = parse.patientRegisterParse(request.GET)
    result = ex.patientregister(datadict)
    return HttpResponse(json.dumps(result))


def appointment_reg(request):
    datadict = parse.app_register_parse(request.GET)
    # print("got here\n data dict")
    # print(datadict)
    info_dict, date_dict = ex.process_app_req_init(datadict=datadict)
    file = [info_dict, date_dict]
    return HttpResponse(json.dumps(file))


def app_reg_final(request):
    datadict = parse.app_reg_final_parse(request.GET)
    result = ex.save_app(datadict)
    return HttpResponse(json.dumps(result))