from appAUDITAI.dataview.MISC.imports import *

class AccessRequestHome(View):

    template_name = 'pages/TICKETS/ticket-home.html'

    def get(self, request):
        user = request.user
        group_names = user.groups.values_list('name', flat=True)
        context = {'user':user, 'group_names':group_names}
        return render(request, self.template_name,context)