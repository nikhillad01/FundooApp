from django.contrib import admin
from .models import stock,Registration,RestRegistration
# Register your models here.
admin.site.register(stock)
admin.site.register(Registration)
admin.site.register(RestRegistration)
