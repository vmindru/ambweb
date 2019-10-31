from django.contrib import admin
from django.conf.urls import url
from django.template.response import TemplateResponse

from live.models import Karts
from live.models import Laps
from live.models import Heats
from live.models import Settings


@admin.register(Heats)
class HeatsAdmin(admin.ModelAdmin):
    list_display = ['heat_id', 'heat_finished', 'first_pass_id', 'last_pass_id', 'rtc_time_start', 'rtc_time_end']
    list_filter = ['heat_finished']


@admin.register(Laps)
class LapsAdmin(admin.ModelAdmin):
    list_display = ['heat_id', 'pass_id', 'transponder_id', 'rtc_time']
    list_filter = ['heat_id']


@admin.register(Karts)
class KartsAdmin(admin.ModelAdmin):
    list_display = ['name', 'kart_number', 'transponder_id']


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['setting', 'value']
    fields = ['value']

    def get_urls(self):
        urls = super(SettingsAdmin, self).get_urls()
        security_urls = [
            url(r'^config/$', self.admin_site.admin_view(self.security_configuration)),
        ]

        return security_urls + urls

    def security_configuration(self, request):
        context = dict(
            self.admin_site.each_context(request),
            something="test",
        )
        return TemplateResponse(request, "config.html", context)

    class Media:
        css = {
            'all': ('css/config.css',)
             }
