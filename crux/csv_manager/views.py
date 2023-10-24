from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .models import CSVData
import csv
import json
import logging
from django.views import View

logger = logging.getLogger(__name__)


# Create your views here.

def home(req):
    return HttpResponse("HOME", req)


@csrf_exempt
def health_check(request):
    if request.method == 'GET':
        # This is a GET request
        # Your code for handling GET requests goes here
        return HttpResponse("Service is online checked using get request")
    elif request.method == 'POST':
        # This is a POST request
        # Your code for handling POST requests goes here
        return HttpResponse("Service is online checked using post request")


class CSVView(APIView):
    # permission_classes = ()
    # authentication_classes = ()
    def post(self, request):
        if request.method == 'POST':
            try:
                logger.debug(f"upload csv endpoint invoked with req: {request}")
                form = CSVUploadForm(request.POST, request.FILES)
                if form.is_valid():
                    # Process the uploaded CSV file
                    csv_file = request.FILES['document']
                    csv_content = csv_file.read().decode('utf-8')
                    # Create an instance of the model with the CSV content
                    instance = CSVData(content=csv_content, **form.cleaned_data)
                    instance.save()
                    ## below approach can also be used.
                    # uploaded_csv = request.FILES.get('document')
                    # logger.info(f"Csv file data: {uploaded_csv}")
                    # decoded_csv = uploaded_csv.read().decode('utf-8')
                    # csv_data = csv.DictReader(decoded_csv.splitlines())
                    #
                    # # Save the data to the database (you can customize this part)
                    # for row in csv_data:
                    #     csv_data_instance = CSVData(**row)
                    #     csv_data_instance.save()
                    return HttpResponse(status=201)
                else:
                    return HttpResponse(status=400,
                                        content="Invalid form data. Required fields: title(CharField),description(CharFeild), document(File)")
            except Exception as e:
                logger.exception(f"Error while storing csv file: {request.FILES}. Error:{e}")
                return HttpResponse(status=500)
        else:
            return HttpResponse(status=405, content="Only POST method allowed.")

    @csrf_exempt
    def get(self, request):
        if request.method == "GET":
            file_id = request.GET.get("file_id")
            logger.debug(f"get csv file endpoint invoked with query param: {file_id}")
            if file_id is not None:
                # Retrieve a specific CSV file by unique ID
                csv_data = get_object_or_404(CSVData, id=file_id)
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{file_id}.csv"'
                response.write(csv_data.document)
                return response  # Return the CSV file as a response
            else:
                # Retrieve all CSV files
                all_csv_data = CSVData.objects.all().values('id', 'document')
                return JsonResponse(list(all_csv_data), safe=False)
                # all_csv_data = CSVData.objects.all().values('id', 'document')
                # response = HttpResponse(content_type='text/csv')
                # response['Content-Disposition'] = 'attachment; filename="all_csv_data.csv"'
                # for csv_data in all_csv_data:
                #     response.write(csv_data['document'])
                # return response  # Return the entire CSV content as a response

        else:
            return HttpResponse(status=405, content="Only POST method allowed.")



class GetCSVData(APIView):
    def get(self,request):
        logger.info(f"Reading data from csv file")
        if request.method == "GET":
            try:
                file_id = request.GET.get("file_id")
                csv_data = get_object_or_404(CSVData, id=file_id)
                response_dict ={
                    "id"  : csv_data.id,
                    "title": csv_data.title,
                    "content": csv_data.content
                }
                return HttpResponse(status=200, content=json.dumps(response_dict))
            except Exception as e:
                logger.exception(f"Exception occurred while reading data from :{CSVData}. Error: {e}")
                return
        else:
            return HttpResponse(status=405, content="Only GET method allowed.")