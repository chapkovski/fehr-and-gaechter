from otree.models import Session
from django.views.generic import TemplateView, ListView
from django.shortcuts import render
from .models import Punishment
from django.http import HttpResponse
from django.template import Context, loader


# the view to get a list of all sessions
class AllSessionsList(TemplateView):
    template_name = 'pggfg_export/all_session_list.html'
    url_name = 'pggfg_sessions_list'
    url_pattern = r'^pggfg_sessions_list/$'
    display_name = 'Exporting punishment data from PGGFG'

    def get(self, request, *args, **kwargs):
        candidates_list = Punishment.objects.filter(amount__isnull=False).values_list('sender__session', flat=True)

        all_sessions = Session.objects.filter(id__in=candidates_list)
        pggfg_sessions = [i for i in all_sessions if 'pggfg' in i.config['app_sequence']]
        return render(request, self.template_name, {'sessions': pggfg_sessions})


class ListPunishmentsView(ListView):
    template_name = 'pggfg_export/punishments_list.html'
    url_name = 'punishments_list'
    url_pattern = r'^session/(?P<pk>[a-zA-Z0-9_-]+)/punishments/$'
    model = Punishment
    context_object_name = 'punishments'

    def get_queryset(self):
        session_code = self.kwargs['pk']
        return Punishment.objects.filter(sender__session__code=session_code,
                                         amount__isnull=False)


class PunishmentCSVExport(TemplateView):
    template_name = 'pggfg_export/punishments.txt'
    url_name = 'punishments_export'
    url_pattern = r'^session/(?P<pk>[a-zA-Z0-9_-]+)/punishments_export/$'
    response_class = HttpResponse
    content_type = 'text/csv'

    def get(self, request, *args, **kwargs):
        ...
        response = HttpResponse(content_type='text/csv')
        session_code = self.kwargs['pk']
        filename = '{}_punishment_data.csv'.format(session_code)
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        punishments = Punishment.objects.filter(sender__session__code=session_code,
                                                amount__isnull=False)
        t = loader.get_template(self.template_name)
        c = {
            'punishments': punishments,
        }
        response.write(t.render(c))
        return response




        # return render(request, self.template_name, {'sessions': all_sessions })
