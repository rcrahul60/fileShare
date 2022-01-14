from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate


# register
@api_view(["POST"])
@permission_classes([AllowAny])
def RegistrationView(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get_or_create(user=user)[0].key
        return Response({'message':"user created successfully","token":token,"status":status.HTTP_201_CREATED})
    else:
        return Response({"error":serializer.errors})

#Login
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')
    try:
        user = authenticate(email = email,password=password)
        if user.is_active:
            token = Token.objects.get_or_create(user=user)[0].key
            return Response({"message":"login successfull","token":token,"status":status.HTTP_200_OK})
        else:
            return Response({"message":"please check you email and password","status":status.HTTP_400_BAD_REQUEST})

    except Exception as e:
        return Response({"message":"login failed","status":status.HTTP_400_BAD_REQUEST})



#File Upload
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def fileCreate(request):
    data=request.data
    data['user']=request.user.id

    serializer = FileSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"File uploaded successfully","status":status.HTTP_200_OK})
    else:
        return Response({"message":"upload Failed","error":serializer.errors,"status":status.HTTP_400_BAD_REQUEST})



#File List
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def fileList(request):
    data = FileUpload.objects.all()
    print(data)
    serializer=FileSerializer(data,many=True,context={'request': request})
    if serializer:
        return Response({"message":"File List","data":serializer.data,"status":status.HTTP_200_OK})
    else:
        return Response({"message":"upload Failed","error":serializer.errors,"status":status.HTTP_400_BAD_REQUEST})



#Single File .....Client can access only
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def SingleFile(request,id):
    if request.user.id==2:
        data = FileUpload.objects.get(id=id)
        serializer=FileSerializer(data,context={'request': request})
        if serializer:
            return Response({"message":"Single File","data":serializer.data,"status":status.HTTP_200_OK})
        else:
            return Response({"message":"Something Went Wrong","error":serializer.errors,"status":status.HTTP_400_BAD_REQUEST})
    else:
        return Response({"message":"Authentication Failed","status":status.HTTP_400_BAD_REQUEST})

