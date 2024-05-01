from django.db import models


class EncryptedFile(models.Model):
    name = models.CharField(max_length=255)
    encrypted_data = models.BinaryField()
    encryption_key = models.CharField(max_length=255)

    def __str__(self):
        return self.name
