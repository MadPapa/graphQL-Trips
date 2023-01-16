from django.db import models

# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=45)
    surname = models.CharField(max_length=45)
    pesel = models.CharField(max_length=11, unique=True)
    phoneNumber = models.CharField(max_length=9, unique=True)

    def __str__(self) -> str:
        return f'{self.name} {self.surname}'


class Hotel(models.Model):
    STARS_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    name = models.CharField(max_length=45)
    phoneNumber = models.CharField(max_length=9)
    website = models.URLField()
    stars = models.CharField(max_length=1, default=1, choices=STARS_CHOICES)

    def __str__(self) -> str:
        return self.name


class Trip(models.Model):
    client = models.ManyToManyField(Client)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True)
    country = models.CharField(max_length=45)
    city = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    checkinDate = models.DateTimeField()
    checkoutDate = models.DateTimeField()

    def __str__(self) -> str:
        return f'{self.country} - {self.city}'
