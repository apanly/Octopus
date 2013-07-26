from django.contrib import admin
from JobsWeb.models import Alertjobhost,Alertgroup, Alertjobalert, Alertjobdatasource, Alertjobdepend, Alertjobdeploy, Alertjoberror, Alertjoblist, AlertjoblistOld, Alertjoblog, AlertjoblogOld, Alertjobmodlog, Alertjobqueue, Alertjobrunlog, Alertjobsystem, Alertlist, Alertlogmodule, Alertmodule, Alertpublish
from JobsWeb.models import UserCenter

admin.site.register(Alertjobhost)
admin.site.register(Alertgroup)
admin.site.register(Alertjobalert)
admin.site.register(Alertjobdatasource)
admin.site.register(Alertjobdepend)
admin.site.register(Alertjobdeploy)
admin.site.register(Alertjoberror)
admin.site.register(Alertjoblist)
admin.site.register(AlertjoblistOld)
admin.site.register(Alertjoblog)
admin.site.register(AlertjoblogOld)
admin.site.register(Alertjobmodlog)
admin.site.register(Alertjobqueue)
admin.site.register(Alertjobrunlog)
admin.site.register(Alertjobsystem)
admin.site.register(Alertlist)
admin.site.register(Alertlogmodule)
admin.site.register(Alertmodule)
admin.site.register(Alertpublish)
admin.site.register(UserCenter)
