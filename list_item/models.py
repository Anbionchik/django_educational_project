from django.db import models
from main.models import ListModel


class ListItemModel(models.Model):
    """ Модель списка дел в списке дел """
    name = models.CharField(max_length=128, verbose_name='Наименование задачи')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    listmodel_id = models.ForeignKey('main.ListModel', on_delete=models.CASCADE)  # Без импорта лучше
    is_done = models.BooleanField(default=False)
    expiration_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        obj = ListModel.objects.filter(id=self.listmodel_id_id).first()
        if all(type(self).objects.filter(listmodel_id=self.listmodel_id).values_list('is_done', flat=True)):
            obj.is_done = True
            obj.save()
        else:
            if obj.is_done:
                obj.is_done = False
                obj.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Список задач'
        unique_together = ('listmodel_id', 'name', 'expiration_date')
