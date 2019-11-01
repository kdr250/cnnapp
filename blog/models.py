from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.storage import default_storage
from io import BytesIO
from PIL import Image

# EXAMPLE_FOO = ((1, 'foo1'), (2, 'foo2'))
cifar_list = (
    ('airplane', '飛行機'), ('automobile', '自動車'), ('bird', '鳥'), ('cat', '猫'), ('deer', '鹿'),
    ('dog', '犬'), ('frog', 'カエル') , ('horse', '馬'), ('ship', '舟'), ('truck', 'トラック')
)


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='タイトル')
    content = models.TextField(verbose_name='投稿内容')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='投稿日',)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='投稿者',)
    image = models.ImageField(default='default.jpg', upload_to=f'uploads/%Y%m%d/', verbose_name='写真',)
    label = models.TextField(choices=cifar_list, null=True, blank=True, verbose_name='ラベル',)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '投稿記事'
        verbose_name_plural='投稿記事'

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

        memfile = BytesIO()

        # img = Image.open(self.image.path)
        img = Image.open(self.image)

        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size, Image.ANTIALIAS)
            img.save(memfile, 'JPEG', quality=95)
            default_storage.save(self.image.name, memfile)
            memfile.close()
            img.close()

