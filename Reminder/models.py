from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    name=models.CharField(max_length=20)
    date=models.DateField(auto_now_add=True)#updates date time field when an instance is created
                                            #auto _add cretaes date time field only the first time the instance is created 
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    """field name = models.ForeignKey(WASD, on_delete = OPERATION TYPE)  """
    completed=models.BooleanField(default=False)
    def __str__(self):
        return self.name