from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from djstripe.models import *
from datetime import datetime, timedelta

# Recovery operators / user models.
class Profile(models.Model):

    #variable to set date for registered users, days = days on todays date added. Can be used for promotional offer for new users
    ddd = datetime.now() + timedelta(days=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50, null= True)
    full_name = models.CharField(max_length=50, null= True)
    mobile_number = models.CharField(max_length=20, null=True)
    profile_image = models.ImageField(null=True)
    profile_summary = models.TextField(max_length=300, null= True)
    city = models.CharField(max_length=100, null= True)
    postcode = models.CharField(max_length=12, null= True)
    latitude = models.FloatField(null = True, blank= True)
    longitude = models.FloatField(null = True, blank= True)
    stripeCustomerId = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255)
    stripePaidDate = models.DateTimeField(default = ddd)
    stripeWebHookStatus = models.CharField(max_length=20, null= True, blank=True)
    
    # returns username as string.
    def __str__(self):
        return self.user.username    

    # For getting the details to display on map. used with GeoDjango format. 
    def serialize(self):
        json_dict = {}
        json_dict['type'] = 'Feature'
        json_dict['properties'] = dict(name=self.company_name, number = self.mobile_number, summary = self.profile_summary)
        json_dict['geometry'] = dict(type='Point', coordinates=list([self.longitude,self.latitude]))
        return(json_dict)
    
    
# For user creation
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# To save user profile.
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()