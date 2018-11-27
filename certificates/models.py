from django.db import models


class Domain(models.Model):
    domain_name = models.CharField(max_length=256, primary_key=True)
    owner = models.ForeignKey('auth.User', related_name="domains", on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.domain_name


class Certificate(models.Model):
    id = models.IntegerField(primary_key=True)
    domain_name = models.ForeignKey(Domain, on_delete=models.CASCADE, db_index=False)
    private_key = models.TextField(blank=True, null=True)
    conf = models.TextField(blank=True, null=True)
    csr = models.TextField(blank=True, null=True)
    crt = models.TextField(blank=True, null=True)
    intermediate = models.TextField(blank=True, null=True)
    valid = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.domain_name.domain_name + "-" + str(self.id)
