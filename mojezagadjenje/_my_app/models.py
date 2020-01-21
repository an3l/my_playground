from django.db import models

# Create your models here.

class table_so2(models.Model):
    _city=models.CharField(max_length=64)
    _location=models.CharField(max_length=64)
    _value=models.IntegerField()
    _date=models.DateTimeField(auto_now=True)
    #duration=models.IntegerField()
    def __str__(self):
        return f"SO2 from {self._city}: {self._value} at {self._date}"

class table_h2s(models.Model):
    _city=models.CharField(max_length=64)
    _location=models.CharField(max_length=64)
    _value=models.IntegerField()
    _date=models.DateTimeField(auto_now=True)
    #duration=models.IntegerField()
    def __str__(self):
        return f"H2S from {self._city}: {self._value} at {self._date}"
class table_no2(models.Model):
    _city=models.CharField(max_length=64)
    _location=models.CharField(max_length=64)
    _value=models.IntegerField()
    _date=models.DateTimeField(auto_now=True)
    #duration=models.IntegerField()
    def __str__(self):
        return f"NO2 from {self._city}: {self._value} at {self._date}"

class table_nox(models.Model):
    _city=models.CharField(max_length=64)
    _location=models.CharField(max_length=64)
    _value=models.IntegerField()
    _date=models.DateTimeField(auto_now=True)
    #duration=models.IntegerField()
    def __str__(self):
        return f"NOX from {self._city}: {self._value} at {self._date}"
class table_no(models.Model):
    _city=models.CharField(max_length=64)
    _location=models.CharField(max_length=64)
    _value=models.IntegerField()
    _date=models.DateTimeField(auto_now=True)
    #duration=models.IntegerField()
    def __str__(self):
        return f"NO from {self._city}: {self._value} at {self._date}"
class table_co(models.Model):
    _city=models.CharField(max_length=64)
    _location=models.CharField(max_length=64)
    _value=models.IntegerField()
    _date=models.DateTimeField(auto_now=True)
    #duration=models.IntegerField()
    def __str__(self):
        return f"CO from {self._city}: {self._value} at {self._date}"
class table_o3(models.Model):
    _city=models.CharField(max_length=64)
    _location=models.CharField(max_length=64)
    _value=models.IntegerField()
    _date=models.DateTimeField(auto_now=True)
    #duration=models.IntegerField()
    def __str__(self):
        return f"03 from {self._city}: {self._value} at {self._date}"
class table_pm10(models.Model):
    _city=models.CharField(max_length=64)
    _location=models.CharField(max_length=64)
    _value=models.IntegerField()
    _date=models.DateTimeField(auto_now=True)
    #duration=models.IntegerField()
    def __str__(self):
        return f"PM10 from {self._city}: {self._value} at {self._date}"
class table_pm25(models.Model):
    _city=models.CharField(max_length=64)
    _location=models.CharField(max_length=64)
    _value=models.IntegerField()
    _date=models.DateTimeField(auto_now=True)
    #duration=models.IntegerField()
    def __str__(self):
        return f"PM2.5 from {self._city}: {self._value} at {self._date}"

