from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connection

Group.objects.get_or_create(name='Utilizador')
Group.objects.get_or_create(name='Treinador')
Group.objects.get_or_create(name='Administrador')
Group.objects.get_or_create(name='Jogador')

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True)
    born = models.DateField(null=True)

    class Meta:
        ordering = ['user']
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)
        if User.objects.count() == 1:
            instance.groups.add(Group.objects.get(name='Administrador'))
        else:
            instance.groups.add(Group.objects.get(name='Utilizador'))


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class clubmodel(models.Model):
    name = models.TextField()
    image = models.ImageField()
    description = models.TextField()
    about = models.TextField()
    contact = models.TextField()

    class Meta:
        ordering = ['id']
        verbose_name = 'Club'
        verbose_name_plural = 'Club'

    def __str__(self):
        return self.name


if clubmodel.objects.count() == 0:
    with connection.cursor() as c:
        c.execute(
            "INSERT INTO website_clubmodel (name, image, description, about, contact) VALUES ('Clube', 'favicon.ico', 'Melhor Clube do Mundo!', 'Sobre nós', 'Qualquer Coisa')")


class echelonmodel(models.Model):
    name = models.TextField()

    class Meta:
        ordering = ['id']
        verbose_name = 'Echelon'
        verbose_name_plural = 'Echelons'

    def __str__(self):
        return self.name


class teammodel(models.Model):
    name = models.TextField()
    trainer = models.ForeignKey(to=User, on_delete=models.CASCADE)
    echelon = models.ForeignKey(to=echelonmodel, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'

    def __str__(self):
        return self.name


class gamemodel(models.Model):
    name = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    team = models.ForeignKey(to=teammodel, on_delete=models.CASCADE)
    enemy = models.TextField()
    teamgoals = models.IntegerField()
    enemygoals = models.IntegerField()

    class Meta:
        ordering = ['id']
        verbose_name = 'Game'
        verbose_name_plural = 'Games'

    def __str__(self):
        return self.name


class trainingmodel(models.Model):
    name = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    team = models.ForeignKey(to=teammodel, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        verbose_name = 'Training'
        verbose_name_plural = 'Trainings'

    def __str__(self):
        return self.name
