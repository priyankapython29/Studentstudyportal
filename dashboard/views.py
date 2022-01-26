from email.mime import audio
from gc import is_finalized
from django.shortcuts import redirect, render
from django.contrib import messages
from . forms import *
from django.views import generic 
from youtubesearchpython import VideosSearch
import requests
import wikipedia

# Create your views here.
def home(request):
    return render(request,'dashboard/home.html') #dashboard-app name,home.html under that app file

def notes(request):
    if request.method =="POST":
        form=NotesForm(request.POST) #store all data in form
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description']) #title & description is textfield name
            notes.save() #save data in db table
        messages.success(request,f"Notes Added from {request.user.username} Successfully!") #when data added successfully display  message on admin panel
        
    else:
        form = NotesForm() #create notes form
        
    notes = Notes.objects.filter(user=request.user) #create object for notes table to display all notes table data on notes  view template #user=request.user->current user-login user
                                                    #pass in that paremeter & that user retrive all data from notes table and store in notes object #set filter for current user 
    context = {'notes':notes,'form':form} #pass that notes object in context variable
    return render(request,'dashboard/notes.html',context) #pass context variable as a 3rd parameter to template

def delete_note(request,pk=None): #pass 1 primery key pk is none
    Notes.objects.get(id=pk).delete() #delete id  row which is pk 
    return redirect("dashboard:notes") #& redirect to notes.html page

class NotesDetailView(generic.DetailView):
    model = Notes
    
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished'] # is_finished from form.py file from class Homeworkform
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished  #finished variable value either it is true or false 
                ) #get all data from form
                
                
            homeworks.save() #save data in db
            messages.success(request,f'Homework Added from {request.user.username}!!')
    else:
        form = HomeworkForm() #create object for homeworkform which is created in forms.py file
    
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        home == True
    else:
       home == False
       
    context = {
              'homeworks':homework,
              'home':home,
              'form':form,
      }
    return render(request,'dashboard/homework.html',context)

def update_homework(request,pk=None): #create fun for check box event 
    homework = Homework.objects.get(id=pk)
    
    if homework.is_finished == True: #when click on checkbox 
        homework.is_finished = False
        print('hello')
    else:
        homework.is_finished = True
        
    homework.save() #save changes in db
   
    return redirect('dashboard:homework')
    
    
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete() #get id of that homework data and delete from db table
    return redirect('dashboard:homework') 
    
    
#youtube session
def youtube(request):
    if request.method == "POST": #when click on search button get post method
        form = DashboardForm(request.POST) #create form object
        text = request.POST['text'] #when click on search button then get text which is write in text field this text is search text
        video = VideosSearch(text,limit=10) #limit=10 display top 10 result 
        result_list = [] #create 1 empty list to store searched result
        for i in video.result()['result']:
            #create 1 dictionery to get values
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
                
            }
            desc = ''
            if i['descriptionSnippet']: #check desc is present
                for j in i['descriptionSnippet']: #check if desc is more then 1 then check
                    desc += j['text']             #if desc present then concatinate
            result_dict['description'] = desc     #assign desc to dictionary description field
            result_list.append(result_dict) #append this dictionary to list
            context={                       #pass form object and result to youtube.html page
                'form':form,
                'results':result_list
            }
            
        return render(request,'dashboard/youtube.html',context)
        
    else:
        form = DashboardForm() #create object of class which is define in forms.py file
    context ={'form':form}
    return render(request,"dashboard/youtube.html",context)

#todo section

def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request,f"Todo Added from {request.user.username}!!")
    else:
        form =TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
        
    context = {
        'form':form,
        'todos':todo,
        'todos_done':todos_done
    }
    return render(request,"dashboard/todo.html",context)


def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('dashboard:todo')


def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('dashboard:todo')

#books section

def books(request):
    if request.method == "POST": #when click on search button get post method
        form = DashboardForm(request.POST) #create form object
        text = request.POST['text'] #when click on search button then get text which is write in text field this text is search text
        url = "https://www.googleapis.com/books/v1/volumes?q="+text #+text is your search text
        r = requests.get(url) #execute this url no present in django install externaly
        answer = r.json() #answer get in answer json object
        result_list = [] #create 1 empty list to store searched result
        for i in range(10):
            #create 1 dictionery to get values #get range(10) 10 records
            result_dict = {
                
                'title':answer['items'][i]['volumeInfo']['title'],# json object format
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink')
                
            }
            
            result_list.append(result_dict) #append this dictionary to list
            context={                       #pass form object and result to youtube.html page
                'form':form,
                'results':result_list
            }
            
        return render(request,'dashboard/books.html',context)
        
    else:
        form = DashboardForm() #create object of class which is define in forms.py file
    context ={'form':form}
    return render(request,"dashboard/books.html",context)


def dictionary(request):
    if request.method == "POST": #when click on search button get post method
        form = DashboardForm(request.POST) #create form object
        text = request.POST['text'] #when click on search button then get text which is write in text field this text is search text
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text #+text is your search text
        r = requests.get(url) #execute this url no present in django install externaly
        answer = r.json() #answer get in answer json object
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms =answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context = {
                'form':form,
                'input':''
            }
        return render(request,"dashboard/dictionary.html",context)
    
    else:
        form = DashboardForm()
    context = {'form':form}
    return render(request,"dashboard/dictionary.html",context)


def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        #geting this information text,link... from wikipedia API 
        context ={
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,"dashboard/wiki.html",context)
    else:
      form = DashboardForm()
      context = {
        'form':form
      }
    return render(request,"dashboard/wiki.html",context)

def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length': #for length
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1'] #yard
                second = request.POST['measure2'] #foot
                input = request.POST['input']
                answer =''
                if input and int(input) >=0: #check input is integer -int(input) & not null
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/3} yard'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
        if request.POST['measurement'] == 'mass': 
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1'] 
                second = request.POST['measure2'] 
                input = request.POST['input']
                answer =''
                if input and int(input) >=0: 
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)*2.20462} pound'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
                
        
    else:
        form = ConversionForm()
        context = {
             'form':form,
             'input':False
         }
    
    return render(request,"dashboard/conversion.html",context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST) #getform from forms.py
        if form.is_valid():  #if form is valid
            form.save()        #save form data in db
            username = form.cleaned_data.get('username') #get username
            messages.success(request,f"Account Created for {username}!!") #display success msg
            return redirect("login")
    else:        
       form = UserRegistrationForm()
       
    context ={
        'form':form
        
     }
    return render(request,"dashboard/register.html",context)


def profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user=request.user) #get all data from hommework table which is not finished for current login user
    todos = Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
        
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
        
    context = {
        'homeworks' : homeworks,
        'todos' : todos,
        'homework_done' : homework_done,
        'todos_done' : todos_done
    }
    
    return render(request,"dashboard/profile.html",context)


    

