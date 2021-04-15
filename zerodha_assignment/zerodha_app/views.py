from django.shortcuts import render
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import SearchForm
from django.views.generic import ListView, DetailView,View
from .models import Item
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from datetime import datetime,timedelta
import csv

def genrate_keys(search_name):
    base = datetime.today()
    numdays=30
    date_list = [base - timedelta(days=x) for x in range(numdays)]
    dates=[dat.strftime('%d%m%y') for dat in date_list]
    date_fin=[search_name+dat for dat in dates]
    return date_fin

# def export(request):
#     print("inside write_csv")
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="file_sample.csv"'
#     form=SearchForm(self.request.POST or None)
#     if form.is_valid():
#         search_name=form.cleaned_data['name']
#         print(search_name)
#         date=datetime.today()
#         lst=genrate_keys(search_name)
#         dict=[]
#         for k in lst:
#             if cache.get(k):
#                 print(cache.get(k))
#                 dict.append(cache.get(k))
#     writer = csv.writer(dict)
#     for em in dict:
#         writer.writerow([em.name,em.code,em.date,em.open,em.high,em.low,em.close])
#     return response

class HomeView(ListView):
    def get(self,*args,**kwargs):
        form=SearchForm()
        context={
                 'form':form
        }
        return render(self.request,"home.html",context)


    def post(self,*args,**kwargs):
        form=SearchForm(self.request.POST or None)
        if form.is_valid():
            search_name=form.cleaned_data['name']
            print(search_name)
            date=datetime.today()
            lst=genrate_keys(search_name)
            dict=[]
            for k in lst:
                if cache.get(k):
                    print(cache.get(k))
                    dict.append(cache.get(k))
            print(dict)
            context={
                    'object':dict
            }
            print(context)
            return render(self.request,'result.html',context)

        else:
            message.info(self.request,"please fill valid information")
