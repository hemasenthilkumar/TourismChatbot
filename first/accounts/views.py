from django.shortcuts import render,HttpResponse

# Create your views here.
def home(request):
    numbers=[1,2,3,4]
    name="hemapriya"
    args={'myName':name,'numbers':numbers}
    return render(request,'accounts/home.html',args)
def answer(request):
    args={'myName':'hema'}
    return render(request,'accounts/home.html',args)
