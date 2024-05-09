from appAUDITAI.dataview.MISC.imports import *
from django.http import HttpResponseNotFound

def error_404(request, exception):
    return render(request, "error/404.html", {})
    
class no_permission(View):
    template_name = 'error/no_permission.html'
    def get(self,request):
        return render(request,self.template_name)
