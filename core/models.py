from django.db import models
from datetime import date, datetime
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Item(models.Model):
    title = models.CharField(max_length = 20, blank = False)
    price = models.IntegerField(blank = False)
    date_enrolled = models.DateField(default = timezone.now)
    available = models.BooleanField(default = True)
    orders_count = models.IntegerField(default = 0, editable = False)

    categories = [
        ('drink', 'Drink'),
        ('snack', 'Snack'),
        ('dessert', 'Dessert'),
        ('NA', 'NA')
    ]
    category = models.CharField(max_length = 20, choices = categories)

    def get_upload_path(instance, filename):
        return '{0}/{1}'.format(instance, filename)
    image = models.ImageField(upload_to = get_upload_path)

    def __str__(self):
        return self.title
    

class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete = models.CASCADE)
    date_issued = models.DateTimeField(default = datetime.now, blank = False)
    fullfilled = models.BooleanField(default = False)

    def __str__(self):
        return self.id 
    

class OrderItem(models.Model):
    '''NOTE:
    this model creates an intermediary table between an order and products. connecting orders and products directly will
    oblige creating more product objects for each order object, we use order items to separate orders and products
    '''
    
    item = models.ForeignKey('Item', on_delete = models.RESTRICT, blank = False)
    order = models.ForeignKey('Order', on_delete = models.RESTRICT, blank = False)
    quantity = models.IntegerField(default = 1, blank = False)

    def __str__(self):
        return self.id
    

class Payment(models.Model):
    order = models.OneToOneField('Order', on_delete = models.CASCADE, editable = False)
    customer = models.CharField(max_length = 20, editable = False)
    net = models.IntegerField(editable = False) 
    discount = models.IntegerField(default = 0, blank = True)

    #overriding the save() method
    def save(self, *args, **kwargs):
        #define customer name
        self.customer = self.order.customer.name
        #define net price
        self.net = sum([orderitem.item.price for i, orderitem in self.order.orderitem_set.all()])

        super().save(*args, **kwargs)

    def __str__(self):
        return "payment for order {}".format(self.order.id)
    

class Reservation(models.Model):
    customer = models.ForeignKey('Customer', on_delete = models.CASCADE, blank = True)
    date_issued = models.DateTimeField(blank = False)
    QR = models.ImageField(upload_to= 'QRs/%Y/%m/%d')    
    count = [
        ('1',1),
        ('2',2),
        ('3',3),
        ('4',4)
    ]
    people_count = models.IntegerField('persons', default = 1, choices = count)

    def __str__(self):
        return self.id
    

class Customer(models.Model):
    name = models.CharField(max_length = 25, blank = False)
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    date_enrolled = models.DateField(default = timezone.now)
    points = models.IntegerField(default = 0, editable = False)
    profits = models.IntegerField(default = 0, editable = False)

    def __str__(self):
        return self.name
