from django.db import models

STATUS = (
    ("draft", "Draft"),
    ("pending", "Pending"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
)

class Company(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self): return self.name

class ModelPerson(models.Model):
    full_name = models.CharField(max_length=200)
    def __str__(self): return self.full_name

class Offer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    model = models.ForeignKey(ModelPerson, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(choices=STATUS, default="draft", max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)

class Contract(models.Model):
    offer = models.OneToOneField(Offer, on_delete=models.CASCADE, related_name="contract", null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    pdf_url = models.URLField(blank=True)
    status = models.CharField(max_length=16, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
