from django.contrib import admin

from .models import Choice, Poll


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class PollAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['question']}),
                 ('Creator', {'fields': ['created_by']})]
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date', 'created_by')
    list_filter = ['pub_date']
    search_fields = ['question', 'created_by']
    list_per_page = 10


admin.site.register(Poll, PollAdmin)
