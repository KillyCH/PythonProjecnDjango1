from django.db import models

# Create your models here.
RATE_CHOICES = (
    (1, '*'),
    (2, '**'),
    (3, '***'),
    (4, '****'),
    (5, '*****'),
)


class Tag(models.Model):                         # мы создали тэг у которого поле есть в названии
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    price = models.FloatField()
    title = models.CharField(max_length=100)
    text = models.TextField(null=True, blank=True)
    # rating = models.IntegerField(choices=RATE_CHOICES, default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)                  # и подвезали тэг с товаром или нааборот потому что тут связь двухсторонняя

    def __str__(self):
        return self.title

    @property
    def rating(self):
        reviews = self.reviews.all()
        count = reviews.count()
        average = 0
        for i in reviews:
            average += i.rating
        try:
            return average / count
        except:
            return 0

    @property
    def filter_reviews(self):
        return [{'id': i.id, 'text': i.text, 'rating': i.rating}
                for i in self.reviews.filter(rating__gt=3)]


class Review(models.Model):             # логика отзыва будет  описана здесь
    text = models.TextField()
    rating = models.IntegerField(choices=RATE_CHOICES, default=5)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.text
