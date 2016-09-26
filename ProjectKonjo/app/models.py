"""
Definition of models.
"""

from django.db import models

# Create your models here.

class BluetoothDevice (models.Model):
    bluetoothaddress = models.CharField(max_length=17, unique=True)
    displayname = models.CharField(max_length=50)

    def __unicode__(self):
        return self.bluetoothaddress