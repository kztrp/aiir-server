from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from .models import Calculation
from .serializers import UserSerializer, GroupSerializer, CalculationSerializer, CustomUserSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from os import system
import socket


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

@csrf_exempt
def calculation_list(request):
    """
    List all code snippets, or create a new calculation
    """
    if request.method == 'GET':
        calculations = Calculation.objects.all()
        serializer = CalculationSerializer(calculations, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
        PORT = 8082  # Port to listen on (non-privileged ports are > 1023)
        method = int(data["is_fermat"])
        number = data["number"]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            data_sent = bytes("{}{}".format(method, number), "utf8")
            print(data_sent)
            s.send(data_sent)
            data_received = s.recv(1024)
            # print('Received', bool(data))
            print('Received', int(data_received))
            data["result"] = bool(int(data_received))
            data['progress'] = 1
        serializer = CalculationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def calculation_detail(request, pk):
    """
    Retrieve, update or delete a code calculation
    """
    try:
        calculation = Calculation.objects.get(pk=pk)
    except Calculation.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CalculationSerializer(calculation)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CalculationSerializer(calculation, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'PATCH':
        data = JSONParser().parse(request)
        print(data)
        serializer = CalculationSerializer(calculation, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        calculation.delete()
        return HttpResponse(status=204)

@csrf_exempt
def calculation_user(request, user):
    """
    Retrieve, update or delete a code calculation
    """
    if request.method == 'GET':
        calculations = Calculation.objects.all().filter(user=user)
        serializer = CalculationSerializer(calculations, many=True)
        return JsonResponse(serializer.data, safe=False)

class CustomUserCreate(APIView):

    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def post(self, request):
        user = User.objects.all().filter(username=request.data["username"])
        for u in user:
            if u.check_password(request.data["password"]):
                json = u.id
                return Response(json, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)