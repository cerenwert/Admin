from django.db import models
from django.utils import timezone
from datetime import date

STATUS = (("active","Active"),("expired","Expired"),("canceled","Canceled"))

class Company(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
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
    status = models.CharField(choices=(("draft","Draft"),("pending","Pending"),("approved","Approved"),("rejected","Rejected"),("sent","Sent")), default="draft", max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    offer_pdf_file = models.FileField(upload_to="offers/%Y/%m/", blank=True, null=True)
    offer_pdf_generated_at = models.DateTimeField(blank=True, null=True)
    def __str__(self): return f"Offer #{self.pk}"

class Contract(models.Model):
    offer = models.OneToOneField(Offer, on_delete=models.CASCADE, related_name="contract", null=True, blank=True)
    service_name = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=16, choices=STATUS, default="active")

    auto_renew = models.BooleanField(default=False)
    renewal_period_months = models.PositiveSmallIntegerField(default=12)

    # YENİ: öneri ne zaman yollandı
    last_renewal_proposal_at = models.DateTimeField(blank=True, null=True)

    pdf_url = models.URLField(blank=True)
    pdf_file = models.FileField(upload_to="contracts/%Y/%m/", blank=True, null=True)
    pdf_generated_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"Contract #{self.pk}"

    @property
    def days_left(self):
        if not self.end_date: return None
        return (self.end_date - date.today()).days

    @property
    def is_active_today(self):
        if not (self.start_date and self.end_date): return False
        today = date.today()
        return (self.start_date <= today <= self.end_date) and self.status == "active"
