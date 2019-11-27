from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# Product class
# title, url, pub_date, votes_total, image, icon, body, pub_date_pretty, hunter

class Product(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    url = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    votes_total = models.IntegerField(default=1)
    icon = models.ImageField(upload_to='images')
    image = models.ImageField(upload_to='images')
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def summary(self):
        if len(self.body) <= 100:
            return self.body
        else:
            return self.body[:100]+' ...'

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')
