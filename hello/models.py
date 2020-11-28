from django.db import models

# Create your models here.

class places(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    Name = models.CharField(max_length=63)
    City = models.CharField(max_length=63)
    Cuisine_Style = models.CharField(max_length=127)
    CommentsAverage = models.IntegerField()
    countofcomments = models.IntegerField()
    click = models.IntegerField()
    Price_Range= models.CharField(max_length=31)
    MAXPRICE = models.IntegerField()
    MINPRICE = models.IntegerField()
    link = models.CharField(max_length=127)
    image_url = models.CharField(max_length=127)

    # def ret(self):
    #     return id,Name,City,Cuisine_Style,CommentsAverage,countofcomments,click,Price_Range,MAXPRICE,MINPRICE,link,image_url

class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)
