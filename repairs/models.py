import random
from django.db import models
from django.utils import timezone

def generate_barcode():
    while True:
        code = str(random.randint(10000000, 99999999))
        if not Repair.objects.filter(id=code).exists():
            return code

class Repair(models.Model):
    STATUS_CHOICES = [
        ('Принято', 'Принято'),
        ('В работе', 'В работе'),
        ('Готово', 'Готово'),
        ('Выдано', 'Выдано'),
    ]

    id = models.CharField("Штрихкод/ID", max_length=20, primary_key=True, default=generate_barcode)
    client_name = models.CharField("ФИО Клиента", max_length=200)
    client_phone = models.CharField("Телефон", max_length=30)
    device_model = models.CharField("Модель техники", max_length=200)
    issue_description = models.TextField("Неисправность", blank=True, default="")
    status = models.CharField("Статус", max_length=30, choices=STATUS_CHOICES, default='Принято')
    completed_works = models.TextField("Выполненные работы", blank=True, default="")
    cost = models.DecimalField("Стоимость", max_digits=10, decimal_places=2, default=0.0)
    accepted_at = models.DateTimeField("Дата принятия", default=timezone.now)
    issued_at = models.DateTimeField("Дата выдачи", null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == 'Выдано' and not self.issued_at:
            self.issued_at = timezone.now()
        elif self.status != 'Выдано':
            self.issued_at = None

        super().save(*args, **kwargs)

        # Автоматическая фиксация каждого изменения в истории
        StatusHistory.objects.create(
            repair=self,
            status=self.status,
            completed_works=self.completed_works
        )

    def __str__(self):
        return f"{self.id} - {self.device_model} ({self.client_name})"

class StatusHistory(models.Model):
    repair = models.ForeignKey(Repair, on_delete=models.CASCADE, related_name='history')
    changed_at = models.DateTimeField("Дата изменения", auto_now_add=True)
    status = models.CharField("Статус", max_length=30)
    completed_works = models.TextField("Выполненные работы", blank=True, default="")

    class Meta:
        ordering = ['-changed_at']
