from django.db import models


class Image(models.Model):
    image = models.ImageField(upload_to='images')


class ImageFace(models.Model):
    image = models.ImageField(upload_to='images_face')


class ImageRubbish(models.Model):
    image = models.ImageField(upload_to='images_rubbish')


