from django.shortcuts import render
from django.http import HttpResponse
from  django.http import HttpRequest
# Create your views here.
import cx_Oracle
from firstapp import execution as ex


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
    print("into appointment")
    if request.method == 'POST':
        print(request.POST.get('fname'))
        for key,value in request.POST.items():
            print(f'key: {key}')
            print(f'value : {value}')

    return render(request, 'firstapp/appointment.html')


def registerpage(request):
    if request.method == 'POST':
        #listA = request.POST.items()
        listA = dict(request.POST).items()
        #print(listA)
        listB = {}
        # for key,value in listA:
        #     print(str(key))
        #     print(request.POST.get(str(key)))

        for key,value in listA:
            listB[str(key)] = request.POST.get(str(key))

        # for x in listA:
        #     print(x)

        #print(listB)
        ex.patientregister(listB)
    return render(request, 'firstapp/register.html')


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
    specialization = request.GET.get('DocDept')
    return render(request, 'firstapp/dropdown_list.html', {'doctors': ex.getDocSelect(specialization)})