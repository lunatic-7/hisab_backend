from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Hisab(models.Model):
    ONLINE_CHOICES = [
        ('online_card', 'Online Card'),
        ('banking', 'Banking'),
        ('zomato', 'Zomato'),
        ('swiggy', 'Swiggy'),
        ('amazon', 'Amazon'),
        ('flipkart', 'Flipkart'),
        ('blinkit', 'Blinkit'),
        ('zepto', 'Zepto'),
        ('others', 'Others'),
    ]

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='hisabs')
    item = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    if_online = models.BooleanField(default=False)
    platform = models.CharField(max_length=20, choices=ONLINE_CHOICES, blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.item} - {self.price}"
