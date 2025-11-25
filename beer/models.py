from django.db import models
from django.contrib.auth.models import User

class Smell(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BitterSmell(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Hop(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    a_acid = models.FloatField(default=0)
    b_acid = models.FloatField(default=0)
    smell = models.ForeignKey(Smell, on_delete=models.CASCADE, blank=True, null=True)
    bitter_or_smell = models.ForeignKey(BitterSmell, on_delete=models.CASCADE, blank=True, null=True)
    quality = models.IntegerField()


class MaltTaste(models.Model):
    name = models.CharField(max_length=100)

class Malt(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    color = models.FloatField()
    sugar = models.IntegerField(blank=True, null=True)
    taste = models.ForeignKey(MaltTaste, on_delete=models.CASCADE, blank=True, null=True)
    bitter = models.FloatField(blank=True, null=True)
    quality = models.IntegerField()

class YeastTaste(models.Model):
    name = models.CharField(max_length=100)

class Yeast(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    fermentability = models.IntegerField(blank=True, null=True)
    sedimentability = models.IntegerField(blank=True, null=True)
    taste = models.ForeignKey(YeastTaste, on_delete=models.CASCADE, blank=True, null=True)
    temp_max = models.IntegerField(blank=True, null=True)
    temp_min = models.IntegerField(blank=True, null=True)
    quality = models.IntegerField()

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    yeast = models.ForeignKey(Yeast, on_delete=models.CASCADE)
    malt = models.ForeignKey(Malt, on_delete=models.CASCADE)

class Brewer(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    volume = models.IntegerField()
    quality = models.IntegerField()
    img = models.ImageField(upload_to='media/', default='media/default.jpg')

class Tank(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    volume = models.IntegerField()
    quality = models.IntegerField()
    img = models.ImageField(upload_to='media/', default='media/default.jpg')

class ContainerType(models.Model):
    name = models.CharField(max_length=100)

class Container(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    volume = models.IntegerField()
    container_type = models.ForeignKey(ContainerType, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='media/', default='media/default.jpg')

class Mill(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    speed = models.IntegerField()
    quality = models.IntegerField()
    img = models.ImageField(upload_to='media/', default='media/default.jpg')

class Beer(models.Model):
    STATUS_CHOICES = [
        ('mash','Mash'),
        ('fermenting','Fermenting'),
        ('ready','Ready'),
    ]
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    volume = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    date_created = models.DateField(auto_now_add=True)

class GameState(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="game_state")
    current_date = models.DateField(default="2025-01-01")
    money = models.PositiveIntegerField(default=5000)

    def __str__(self):
        return f"{self.user.username} — ${self.money}"


class BrewerInventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brewer = models.ForeignKey(Brewer, on_delete=models.CASCADE)
    quality = models.PositiveIntegerField(default=100)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.brewer.name} ({self.user.username})"


class HopInventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hop_inventory")
    hop = models.ForeignKey(Hop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    freshness = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.hop.name} x {self.quantity}"


class MaltInventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="malt_inventory")
    malt = models.ForeignKey(Malt, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    freshness = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.malt.name} x {self.quantity}"


class YeastInventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="yeast_inventory")
    yeast = models.ForeignKey(Yeast, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    freshness = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.yeast.name} x {self.quantity}"