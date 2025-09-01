from django.contrib import admin

from main.models import District, State


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
