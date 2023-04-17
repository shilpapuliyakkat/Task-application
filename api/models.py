from django.db import models
from django.contrib.auth.models import User



class Tasks(models.Model):
    task_name=models.CharField(max_length=50)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.task_name


# Create your models here.
