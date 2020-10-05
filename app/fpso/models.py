from django.db import models


class Vessel(models.Model):
    code = models.CharField(max_length=10, unique=True, null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.code)


class Equipment(models.Model):
    ACTIVE = 1
    INACTIVE = 0
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive')
    ]

    name = models.CharField(max_length=40, null=False, blank=False)
    code = models.CharField(max_length=10, unique=True, null=False, blank=False)
    location = models.CharField(max_length=10, null=False, blank=False)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    vessel = models.ForeignKey('Vessel', on_delete=models.CASCADE, null=True, blank=True)

    def activate(self):
        self.status = self.ACTIVE
        self.save()

    def deactivate(self):
        self.status = self.INACTIVE
        self.save()
    
    def get_status(self):
        return 'Active' if self.status == self.ACTIVE else 'Inactive'

    @classmethod
    def get_status_options(self, value):
        opt_map = {status.lower(): value for value, status in self.STATUS_CHOICES }
        return opt_map.get(value)
    
    def __str__(self):
        return '{} - {}'.format(self.code, self.name)