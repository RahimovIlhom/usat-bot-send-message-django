from django.db import models

LANGUAGES = (
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
    ('en', 'English'),
)

APPLICATION_STATUS = (
    ('DRAFT', 'QORALAMA'),
    ('SUBMITTED', 'ARIZA YUBORILDI'),
    ('REJECTED', 'ARIZA RAD ETILDI'),
    ('ACCEPTED', 'ARIZA QABUL QILINDI'),
    ('EXAMINED', 'IMTIHON TOPSHIRDI'),
    ('FAILED', 'IMTIHON MUVAFFAQIYATSIZ'),
    ('PASSED', 'IMTHONDAN MUVAFFAQIYATLI O\'TDI'),
)


class TelegramUser(models.Model):
    tg_id = models.CharField(max_length=255)
    status = models.CharField(max_length=25, choices=APPLICATION_STATUS, null=True, blank=True)
    lang = models.CharField(max_length=2, choices=LANGUAGES, default='uz')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tg_id
