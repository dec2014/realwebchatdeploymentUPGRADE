from django.db import models
from account.models import User

# Create your models here.


class Room(models.Model):
    WAITING='waiting'
    ACTIVE='active'
    CLOSED='closed'

    choices_status=(
        (WAITING,'Waiting'),
        (ACTIVE,'Active'),
        (CLOSED,'Closed')
    )
    room_name=models.CharField(max_length=255,unique=True)
    # client=models.ForeignKey(User,on_delete=models.SET_NULL)
    # agent=models.ForeignKey(User,on_delete=models.SET_NULL)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    # url=models.CharField(max_length=200,blank=True)
    status=models.CharField(max_length=20,choices=choices_status,default=WAITING)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-created_at',)
    def __str__(self):
        return f'{self.room_name}'


class Messages(models.Model):
    body=models.TextField()
    
    created_at=models.DateField(auto_now_add=True)
    created_by=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    class Meta:
        ordering=('created_at',)
    def __str__(self):
        return f'{self.created_by}'
    
class Participants(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.PROTECT)