from django.views.generic import TemplateView
from django.shortcuts import render
from home.forms import HomeForm
from .utilities import user,r1
# Create your views here.
class HomeView(TemplateView):
    template_name='home/mainpage.html'
    def get(self,request):
        form=HomeForm()
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form=HomeForm(request.POST)
        if(form.is_valid()):
            text=form.cleaned_data['query']
            ans=user(text)
            if ans=="":
                ans="I couldn't understand your query!"
            area2=r1()
            form=HomeForm()
        args={'form':form,'text':text,'answer':ans,'revs':area2}
        return render(request,self.template_name,args)

