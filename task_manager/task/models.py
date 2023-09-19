from django.db import models


class Photo(models.Model):
    image = models.ImageField(upload_to='task_photos/')
    def __str__(self):
        return self.image.name

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    priority = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
    )
    is_completed = models.BooleanField(default=False)
    photos = models.ManyToManyField(Photo, blank=True)  # Use a ManyToMany relationship for multiple photos
    task_user_id = models.CharField(max_length=255)
    def __str__(self):
        return self.title
