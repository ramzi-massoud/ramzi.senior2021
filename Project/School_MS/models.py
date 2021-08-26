from django.db import models
from django.contrib.auth.models import User


# Create your models here.

#included in student profile and courses
major = (
    ('Computer Science','1.Computer Science'),
    ('Business','2.Business'),
)
class StudentProfile(models.Model):
    """
    Campuses Tuple dropdown list as a sort of campuses
    Major Tuple dropdown list for majors
    User is provided by django auth user library
    The table holds all personal information about students
    """
    campuses = (
        
        ('Beirut','1.Beirut'),
        ('Baabda','2.Baabda'),
        ('Byblos','3.Byblos')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='df.png')
    major = models.CharField(max_length=255,choices=major,null=True,blank=True)
    phone_nb=models.CharField(max_length=255)
    campus = models.CharField(max_length=255,choices=campuses,null=True,blank=True)
    date_of_birth = models.DateField()

    def __str__(self):
        #return self.user , str(self.major)
        return '{} : {}'.format(self.user, self.major)



    
class AllCourses(models.Model):
    """
    Table displays all courses regardless of user
    This table provides joins for other table (base Table)
    """ 
    courses_name = models.CharField(max_length=255, default="TBA",unique=True)
    code = models.CharField(max_length=5,null=True)
    department = models.CharField(max_length=255,choices=major,null=True,blank=True)
    price = models.FloatField(max_length=25)


    def __str__(self):
        return self.code
    

class Courses(models.Model):
    """
    Table joins with User(StudentProfile),code(AllCourses)
    Add course for users (ONE TO Many)
    """
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)#relation
    courses_name = models.CharField(max_length=255, default="TBA",unique=True)
    code = models.OneToOneField(AllCourses,related_name='Code_FK',on_delete=models.CASCADE)#relation
    department = models.CharField(max_length=255,choices=major,null=True,blank=True)
    time = models.CharField(max_length=255,null=True,default="TBA")
    grade = models.CharField(max_length=3,null=True,default="Not Available Yet")

    def __str__(self):
        if self is not None:
            return str(self.courses_name)
                

class Announcement(models.Model):
    """
    Announcement table with Description of Announcement and date
    """
    desc = models.TextField()
    date = models.DateField()
    
    def __str__(self):
        return self.desc
    
    

    
    