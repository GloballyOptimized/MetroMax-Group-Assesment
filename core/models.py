from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.name
    
#................................................................................................
    
class Blog(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    content = models.TextField()

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
    
#.................................................................................................

class Author(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField()
    photo = models.ImageField(upload_to='authors/')

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    publication_date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='books/')

    def __str__(self):
        return self.title
    
#....................................................................................................

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"Review for {self.book.title}"
    

#......................................................................................................

class Account(models.Model):
    ACCOUNT_TYPES = (
        ('Savings', 'Savings'),
        ('Credit', 'Credit'),
    )

    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)

    def __str__(self):
        return self.account_number
    
class Customer(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    accounts = models.ManyToManyField(Account)

    def __str__(self):
        return self.name

#...........................................................................................................

class Shipment(models.Model):
    STATUS_CHOICES = (
        ('en-route', 'En Route'),
        ('early', 'Early'),
        ('on-time', 'On Time'),
        ('delayed', 'Delayed'),
    )

    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    expected_delivery_date = models.DateField()
    actual_delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='en-route')

    def calculate_delivery_status(self):
        if self.actual_delivery_date:
            if self.actual_delivery_date < self.expected_delivery_date:
                return 'early'
            elif self.actual_delivery_date > self.expected_delivery_date:
                return 'delayed'
            else:
                return 'on-time'
        else:
            return 'en-route'

    def save(self, *args, **kwargs):
        self.status = self.calculate_delivery_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Shipment from {self.origin} to {self.destination}'

    class Meta:
        ordering = ['expected_delivery_date']

class Cargo(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Tracking(models.Model):
    STATUS_CHOICES = (
        ('packing', 'Packing'),
        ('arrived_at', 'Arrived At'),
        ('dispatched_from', 'Dispatched From'),
        ('delivered', 'Delivered'),
    )

    shipment = models.OneToOneField(Shipment, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='packing')
    location = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if self.status == 'delivered':
            self.shipment.actual_delivery_date = timezone.now().date()
            self.shipment.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Tracking for Shipment: {self.shipment}'