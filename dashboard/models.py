from django.db import models
from django.contrib.auth.models import User #when we create super user then automatic created User table,on every project one user default user table
from django.db.models.deletion import CASCADE 

# Create your models here.

class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE) #when user delete then  also notes deleted from db table use CASCADE ,User -user table use foreignkey
                                                     #in notes table need user foreignkey bcoz user created notes use userid in notes table
    title = models.CharField(max_length=200)
    description = models.TextField()   
    
    def __str__(self):
        return self.title #to display notesobject(1) insted of this name it return title (history,gerography)which is set on add notes time and display on dashboard
    
    class Meta:
        verbose_name = "notes"
        verbose_name_plural = "notes"  #to change the notess extra s from admin,dashboard notes table which is display in chrome                 
        
class Homework(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title         
    
class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title                 