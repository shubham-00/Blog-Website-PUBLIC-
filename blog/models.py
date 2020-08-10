from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from PIL import Image
from django.core.exceptions import ValidationError


def file_size(value):
    limit = 0.3 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("File should not be larger than 300KB!")




class Post(models.Model):
    title = models.CharField(max_length=500)

    date_posted = models.DateTimeField(auto_now_add=True)
    # auto_now => every time we edit post, it will change date and time in database
    # auto_now_add => date and time will be of when we created post.

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    CATEGORY_CHOICES = (
        ("future", "Future"),
        ("technology", "Technology"),
        ("health", "Health"),
        ("science", "Science"),
        ("travel", "Travel"),
        ("business", "Business"),
        ("work", "Work"),
        ("culture", "Culture"),
        ("food", "Food"),
        ("programming", "Programming"),
        ("design", "Design"),
        ("politics", "Politics"),
        ("relationships", "Relationships"),
        ("self", "Self"),
        ("startups", "Startups"),
        ("cryptocurrency", "Cryptocurrency"),
    )

    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    likes = models.IntegerField(default=0)

    image = models.ImageField(
        upload_to="blog-images",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]), file_size],
    )

    # text_file = models.FileField(
    #     upload_to="text_files",
    #     validators=[FileExtensionValidator(allowed_extensions=["txt"])],
    # )

    text_file = models.TextField()

    def __str__(self):
        return str(self.id) + " => " + self.title

    def get_description_snippet(self):
        return "{} ...".format(self.text_file[:200])


#    def save(self, *args, **kwargs):
#        super().save()

#        if self.image:
#            img = Image.open(self.image.path)

#            if img.height > 500 or img.width > 500:
#                output_size = (500, 500)
#                img.thumbnail(output_size)
#                img.save(self.image.path)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_Like = models.DateTimeField(auto_now_add=True)


class Follower(models.Model):
    leader_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="leader_user"
    )
    follower_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower_user"
    )
    created_Follower = models.DateTimeField(auto_now_add=True)
