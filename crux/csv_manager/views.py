from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .models import CSVData, CSVConfig
from .serializers import CSVConfigSerializer
from .utilities import get_csv_config, get_possible_graphs, get_relevant_charts
import json
import logging



logger = logging.getLogger(__name__)


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
            ##-------Uncomment this code to store any kind of data----#####
                    # csv_file = request.FILES['document']
                    # csv_content = csv_file.read().decode('utf-8')
                    # csv_title = request.data['title']
                    # description = request.data['description']
                    # instance = CSVData(content=csv_content,description=description,title =csv_title)
                    # instance.save()
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
                    "id": csv_data.id,
                    "title": csv_data.title,
                    "content": csv_data.content
                }
                return HttpResponse(status=200, content=json.dumps(response_dict))
            except Exception as e:
                logger.exception(f"Exception occurred while reading data from :{CSVData}. Error: {e}")
                return
        else:
            return HttpResponse(status=405, content="Only GET method allowed.")



class GetConfig(APIView):
    """
    - Params :
    file_id => csv_file id who's config has to be prepared.
    possible_graphs => Boolean value indicating if possible graphs have to be provided in response or not.

    """
    def get(self,request):
        file_id = request.GET.get("file_id")
        possible_graphs = request.GET.get("possible_graphs")
        if file_id is None:
            return HttpResponse(status="400",content="Please provide the file_id for creating the config")
        csv_file_obj = get_object_or_404(CSVData, id=file_id)
        csv_data = csv_file_obj.content
        csv_config = get_csv_config(csv_data)

        response_dict = {
            "file_id": file_id,
            "csv_config": csv_config
        }
        if possible_graphs:
            possible_graphs = get_possible_graphs(csv_config)
            response_dict["possible_graphs"] = possible_graphs

        return HttpResponse(status="200",content=json.dumps(response_dict))


class GetPossibleGraphs(APIView):
    def post(self, request):
        csv_config = request.POST.get("csv_config")
        csv_config = request.data["csv_config"]
        if csv_config is None:
            return HttpResponse(status="400", content="Please provide the csv_config for getting possible graphs")
        possible_graphs = get_possible_graphs(csv_config)
        logger.info(f"Possible graphs: {possible_graphs}")
        return HttpResponse(status="200", content=json.dumps(possible_graphs))


class SaveConfig(APIView):
    def post(self,request):
        file_id = request.data["file_id"]
        file_config = request.data["file_config"]
        update_if_config_exists = request.data.get("update",False)
        try:
            try:
                csv_data_instance = get_object_or_404(CSVData, id=file_id)
            except CSVData.DoesNotExist:
                # Handle the case where the CSVData instance does not exist
                return HttpResponse(status=404, content="No file with provided file_id")

            for key, val in file_config.items():
                if not key or not val:
                    return HttpResponse(status=400,content="Please ensure there are not null or empty fields in file config")

            delimiter = ';'
            try:
                csv_config_instance = get_object_or_404(CSVConfig,csv_data=csv_data_instance,file_config=file_config)
                print(csv_config_instance)
            except Http404 as e:
                logger.debug(f"No csv config instance found in db")
                logger.info(f"Creating config for the file: {file_id}. Config: {file_config}")
                csv_config_instance = CSVConfig(
                    csv_data=csv_data_instance,
                    delimiter=delimiter,
                    file_config=file_config
                )
            if csv_config_instance:
                if update_if_config_exists:
                    logger.info(f"Updating the config of the file in db to: {file_config}")
                    csv_config_instance.file_config = file_config
                else:
                    logger.info("Returning existing config of the file in db")
                    return JsonResponse({"file_id": file_id, "file_config": csv_config_instance.file_config})


            csv_config_instance.save()

        except Exception as e:
            logger.exception(f"Error occured while storing configuration of the file. Error: {e}")
            return HttpResponse(status=500,content=e)

        return JsonResponse({"file_id":file_id,"file_config": csv_config_instance.file_config})



class QnA(APIView):
    def post(self,request):
        question = request.data["question"]
        all_csv_configs = CSVConfig.objects.all()
        each_file_data =[]
        for csv_config in all_csv_configs:
            print(csv_config.file_config)
            each_file_data.append({
                "file_config":csv_config.file_config,
                "possible_charts":get_possible_graphs(csv_config.file_config)
            })

        answer = get_relevant_charts(question,each_file_data)
        logger.info(f"Answer: {answer}")
        return JsonResponse({"question":question,"answer":answer})
