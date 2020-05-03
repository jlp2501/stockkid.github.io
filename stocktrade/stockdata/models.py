from django.db import models


class Portfolio(models.Model):
    ticker = models.CharField(max_length=10)

    def __str__(self):
        return self.ticker
