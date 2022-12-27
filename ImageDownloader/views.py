from time import sleep
from django.shortcuts import render
from .forms import search_form
from .soup import dl
from django.http import JsonResponse
from django.core import serializers

process = 0
total = 0
alist = []
ilist = []

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
      # a = serializers.serialize('json',alist)
      # b = serializers.serialize('json',ilist)
      a = str(alist)
      b = str(ilist)
      return JsonResponse({'p':process,'t':total,'s':d,'a':a,'b':b})

   return render(request,temp,{'form':form,'message':msg})

def set_process(i):
   global process
   process = i
   return i
def set_total(i):
   global total
   total = i
   return i
def set_alist(a):
   global alist
   alist = a
   return a
def set_ilist(b):
   global ilist
   ilist = b
   return b   