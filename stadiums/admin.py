from django.contrib.gis import admin as gis_admin
from .models import Stadium


class StadiumAdmin(gis_admin.ModelAdmin):
    list_display = ('name', 'owner', 'price_per_hour', 'is_active', 'created_at')
    list_filter = ('is_active', 'owner')
    search_fields = ('name', 'address', 'owner__name')

    fields = ('owner', 'name', 'address', 'price_per_hour', 'location', 'is_active')

    gis_widget_kwargs = {
        'attrs': {
            'default_lon': 69.279619,
            'default_lat': 41.311081,
            'default_zoom': 12,
        },
    }

    class Media:
        js = [
            'stadiums/js/get_location.js',
        ]

    def save_model(self, request, obj, form, change):
        if not obj.owner_id:
            if request.user.role == 'owner':
                obj.owner = request.user

        super().save_model(request, obj, form, change)


gis_admin.site.register(Stadium, StadiumAdmin)




