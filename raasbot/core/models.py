from django.db import models
from django.contrib.auth.models import User as BaseUser

from .utils import get_token

# Create your models here.
class User(models.Model):
    user = models.OneToOneField(BaseUser, blank=True, null=True, on_delete=models.SET_NULL, related_name='user') # currently blank
    token = models.CharField(max_length=32, default=get_token, primary_key=True, unique=True, )

    def __str__(self) -> str:
        return f"{ self.user.username }"

class Bot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bots')
    token = models.CharField(max_length=64, unique=True, primary_key=True)
    is_alive = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{ self.user} - {self.token}"

class ScrapedUser(models.Model):
    person_id = models.CharField(max_length=128, unique=True, primary_key=True)
    scrap_id = models.BigIntegerField(unique=False)
    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, related_name='scraped_users', on_delete=models.CASCADE)
    texted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}"

class UserMessageData(models.Model): # guild to scrape
    user = models.ForeignKey(User, related_name='text_data', on_delete=models.CASCADE)
    guild = models.BigIntegerField()
    channel = models.BigIntegerField()
    guild_invite = models.CharField(max_length=40)
    def __str__(self) -> str:
        return f"{ self.user} - {self.guild_invite}"

class Message(models.Model): # advert texts
    user = models.ForeignKey(User, related_name="dms", on_delete=models.CASCADE)
    topic = models.CharField(max_length=20)
    invite_info = models.CharField(max_length=128)
    guild_invite = models.CharField(max_length=40)
    def __str__(self) -> str:
        return f"{ self.user} - {self.topic}"

class Text(models.Model):
    user = models.ForeignKey(User, related_name='inbox', on_delete=models.CASCADE)
    dm_from = models.ForeignKey(ScrapedUser, on_delete=models.CASCADE)
    dm_to = models.ForeignKey(Bot, on_delete=models.CASCADE)
    data = models.TextField()

class RestrictedRoles(models.Model):
    name = models.CharField(max_length=32)
    text_data = models.ForeignKey(UserMessageData, on_delete=models.CASCADE, related_name="roles")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}"

class LogData(models.Model):
    user = models.ForeignKey(User, related_name='log', on_delete= models.CASCADE)
    target = models.ForeignKey(ScrapedUser, related_name='log', on_delete= models.CASCADE)
    success = models.BooleanField()
    def __str__(self) -> str:
        return f"{self.target}"