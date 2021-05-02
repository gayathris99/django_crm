from django.db import models
from django.db.models.signals import post_save , pre_save
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_organiser = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE )
    def __str__(self):
        return self.user.username
    

class Lead(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE )
    agent = models.ForeignKey(Agent , on_delete = models.SET_NULL, blank=True, null= True)
    category = models.ForeignKey("Category" ,related_name= "leads", on_delete=models.SET_NULL, null = True , blank = True)

    def __str__(self):
        return self.first_name


def post_user_created_signal(sender , instance, created, **kwargs):
    print(instance,created)
    if created:
        UserProfile.objects.create(
            user = instance
        )

post_save.connect(post_user_created_signal, sender = User)



class Category(models.Model):
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


    def __str__(self):
        return self.name