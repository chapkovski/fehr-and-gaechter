from django.conf.urls import url, include
from pggfg import views as v
from django.conf import settings
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(v.ListPunishmentsView.url_pattern, v.ListPunishmentsView.as_view(), name=v.ListPunishmentsView.url_name),
    url(v.PunishmentCSVExport.url_pattern, v.PunishmentCSVExport.as_view(), name=v.PunishmentCSVExport.url_name),
]
