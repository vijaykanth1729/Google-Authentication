from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .forms import BookForm
from .models import Book

#for class based views we can use below imports
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    count_of_users = User.objects.count()
    return render(request,'home.html' , {'count':count_of_users})

def signup(request):
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
         form = UserCreationForm()
    return render(request,'registration/signup.html', {'form':form})


@login_required()
def secret_page(request):
    return render(request,'secret.html')


class Secret_page(LoginRequiredMixin,TemplateView):  #LoginRequiredMixin provides security for the route , if you are logged in then only able to access..
    template_name = 'secret2.html'




#################################
#####Uploading Files#############
#################################
'''
every file should be uploaded using POST request

form should include, enctype='multipart/form-data'

files are stored in REQUEST.FILES object in server

we can use the key to grab the Uploaded file

to save the files on the local machine we need to set configuration

MEDIA_ROOT, MEDIA_URL AND settings  in settings.py file

after configuration we can handle the stored files in two way

*using FileSystemStorage which is a class built in django

*using Model form files like FileField and ImageField
'''

def upload(request):
    context = {}
    if request.method=="POST":
        uploaded_file = request.FILES['document']
        # print(uploaded_file.name)
        # print(uploaded_file.size)
        fs = FileSystemStorage()
        #file system object calls method save and take parameters called name and content
        name = fs.save(uploaded_file.name,uploaded_file)
        context['url ']= fs.url(name)

    return render(request,'upload.html', context)



#Model forms is a best way to store and retrieve a file..
@login_required()
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html',{'books':books})

@login_required()
def upload_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request,'upload_book.html',{'form':form})


@login_required()
def delete_book(request, pk):
    if request.method == "POST":
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')