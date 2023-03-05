from django.shortcuts import render
from .models import Product, Tag


# Create your views here.
def index(request):
    # make calls to database API to get latest pending products to be put in context
    products = Tag.objects.filter(name="P")[0].members.all()
    context = {
        'product_list': products
    }
    return render(request, 'store/index.html', context)

def sold(request):
    products = Tag.objects.filter(name="S")[0].members.all()
    context = {
        'product_list': products
    }
    return render(request, 'store/sold.html', context)

def approved(request):
    products = Tag.objects.filter(name="A")[0].members.all()
    context = {
        'product_list': products
    }
    return render(request, 'store/approved.html', context)

def kicked_back(request):
    products = Tag.objects.filter(name="K")[0].members.all()
    context = {
        'product_list': products
    }
    return render(request, 'store/kicked-back.html', context)

def denied(request):
    products = Tag.objects.filter(name='D')[0].members.all()
    context = {
        'product_list': products
    }
    return render(request, 'store/denied.html', context)