from time import sleep
from django.shortcuts import render
from .forms import search_form
from .soup import dl
from django.http import JsonResponse

process = 0
total = 0

def index(request):
   aj = request.headers.get('x-requested-with') == 'XMLHttpRequest'

   temp = 'index.html'
   msg = ""
   d = False

   if request.method == 'POST' and not aj:

      form = search_form(request.POST)

      msg = request
      if form.is_valid():
         url = form.cleaned_data['url']
         d = dl(url)
         sleep(3)
   form = search_form()

   if aj:
      return JsonResponse({'p':process,'t':total,'s':d,'a':1})

   return render(request,temp,{'form':form,'message':msg})

def set_process(i):
   global process
   process = i
   return i
def set_total(i):
   global total
   total = i
   return i