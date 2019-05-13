from django.contrib import admin
from .models import Airport, Flight, Passenger
# Register your models here.

admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Passenger)
admin.site.site_header = 'My project'                    # default: "Django Administration"
admin.site.index_title = 'Features area'                 # default: "Site administration"
admin.site.site_title = 'My project adminsitration' # default: "Django site admin"
