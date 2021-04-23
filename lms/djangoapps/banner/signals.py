"""
Signal related to banner

"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Banner
from django.contrib.sites.shortcuts import get_current_site
from logging import getLogger
log = getLogger(__name__)

@receiver(post_save, sender=Banner)
def capture_image_url(sender, instance, created, **kwargs):
    try:
        domain = str(get_current_site(request=None))
    except Exception as ex:
        log.error("Error while trying to fetch sites from DB in banner APP Signals.py"+str(ex))
    http  = "http://"
    if created and domain:
        instance.banner_img_url_txt= http+domain+str(instance.banner_img.url)
        instance.save()
        log.info("******Saved banner url successfully******")
    else:
        """prevent the loop back to post_save in case of update call
           pls refer this https://code.djangoproject.com/ticket/28970
        """
        Banner.objects.filter(pk=instance.id).update(banner_img_url_txt = http+domain+str(instance.banner_img.url) if domain else str(instance.banner_img.url))
        log.info("******Updated banner url/other param successfully******")




