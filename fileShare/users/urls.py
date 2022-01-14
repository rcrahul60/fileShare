from django.urls import path,include
from .views import *

urlpatterns = [
    
    path('register/',RegistrationView,name="registerView"),
    path('login/',login,name="login"),
    path('fileupload/',fileCreate,name="fileUpload"),
    path('files/',fileList,name="fileList"),
    path('singlefile/<int:id>/',SingleFile,name="singleFile")

]