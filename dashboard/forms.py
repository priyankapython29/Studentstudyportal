from django import forms 
from . models import *
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm

#link with models.py file with forms.py file

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description'] #set column name from models.py file notes section which is you want to display not id
        
class DateInput(forms.DateInput):
    input_type = 'date'
    
class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due':DateInput()}
        fields = ['subject','title','description','due','is_finished']
        
#create common class for wikipedia search,dictionary search,youtube search like for that create common class DashboardForm
      
class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100,label="Enter Your Search : ")#comman field form search and create object in view file
    
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']
        
class ConversionForm(forms.Form): 
    CHOICES = [('length','Length'),('mass','Mass')] #create 2 radiobutton for length,Mess implement this form on view page
    measurement = forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect)
    
class ConversionLengthForm(forms.Form):        #this class for length
    CHOICES = [('yard','Yard'),('foot','Foot')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput #for input field /box
                            (
        attrs = {'type':'number','placeholder':'Enter the Number'} 
        
    ))
    measure1 = forms.CharField(
        label='',widget= forms.Select(choices = CHOICES) #create 2 function for yard to conver foot to length
    )
    measure2 = forms.CharField(
        label='',widget = forms.Select(choices = CHOICES)
    )
    
    
class ConversionMassForm(forms.Form):        #this class for length
    CHOICES = [('pound','Pound'),('kilogram','Kilogram')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput #for input field /box
                            (
        attrs = {'type':'number','placeholder':'Enter the Number'} 
        
    ))
    measure1 = forms.CharField(
        label='',widget= forms.Select(choices = CHOICES) #create 2 function for pound to conver kilogram to mass
    )
    measure2 = forms.CharField(
        label='',widget = forms.Select(choices = CHOICES)
    )
    
    
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
    