from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=500)
    date = models.DateTimeField("Date")

    def __str__(self):
        return f"{self.title}, {self.text}, {self.date}"
