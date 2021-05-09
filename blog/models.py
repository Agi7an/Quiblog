from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class Question(models.Model):
    question_text = models.TextField(max_length = 300)
    date_posted = models.DateTimeField(default = timezone.now)
    answer = models.CharField(max_length = 100, null = True)
    description = models.TextField(null = True, blank = True)
    category = models.CharField(max_length = 100, blank = True)
    question_image = models.ImageField(null = True, blank = True, upload_to = 'question_pics/')
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse('question-detail', kwargs = {'pk' : self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.question_image:
            img = Image.open(self.question_image.path)
            if img.height > 500 or img.width > 700:
                output_size = (500, 700)
                img.thumbnail(output_size)
                img.save(self.question_image.path)

    @property
    def image_url(self):
        if self.question_image:
            return self.question_image.url
        else:
            return '#'

    


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length = 100)
    votes = models.IntegerField(default = 0)

    def __str__(self):
        return self.choice_text