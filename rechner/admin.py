from django.contrib import admin

from .models import ArbitrationBoard, Commune, Section

# Register your models here.


@admin.register(ArbitrationBoard)
class ArbitrationBoardAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'section',
        'address',
        'allg_kostensteigerung_type',
        'allg_kostensteigerung_value',
        'is_landloard_required',
    )
    search_fields = (
        'name',
        'section',
        'address',
    )


@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = (
        'section',
        'zip_code',
        'name',
    )

    search_fields = (
        'name',
        'section',
        'zip_code',
    )


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'commune')
    search_fields = ('name', 'commune')
