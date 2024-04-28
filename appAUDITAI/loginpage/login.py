from django.shortcuts import render, redirect
from django.views import View

class LoginUser(View):

    template_name = 'pages/dashboard.html'

    def get(self,request):
            return render(request,self.template_name)