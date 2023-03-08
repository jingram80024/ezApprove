from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Product, Tag, TagInfo
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
import json




### page requests ###

@permission_required("store.view_product", login_url="/store/login")
def index(request):
    # make calls to database API to get latest pending products to be put in context
    products = Tag.objects.filter(name="P")[0].members.all()
    context = {
        'product_list': products
    }
    return render(request, 'store/index.html', context)


@permission_required("store.view_product", login_url="/store/login")
def sold(request):
    products = Tag.objects.filter(name="S")[0].members.all()
    context = {
        'product_list': products
    }
    return render(request, 'store/sold.html', context)


@permission_required("store.view_product", login_url="/store/login")
def approved(request):
    products = Tag.objects.filter(name="A")[0].members.all()
    context = {
        'product_list': products
    }
    return render(request, 'store/approved.html', context)


@permission_required("store.view_product", login_url="/store/login")
def kicked_back(request):
    products = Tag.objects.filter(name="K")[0].members.all()
    context_list = []
    for product in products:
        taginfo = TagInfo.objects.filter(product=product)[0]
        context_list.append([product, taginfo])
    context = {
        'context_list': context_list
    }
    return render(request, 'store/kicked-back.html', context)


@permission_required("store.view_product", login_url="/store/login")
def denied(request):
    products = Tag.objects.filter(name='D')[0].members.all()
    context = {
        'product_list': products
    }
    return render(request, 'store/denied.html', context)





### database manipulation requests ###

def swap_tag_helper(request, action, tag_name, response_msg="", reason="none"):
    response = {
        'status': 0,
        'message': 'ERROR: database not updated, something went wrong.'
    }
    if request.method == "POST":
        if request.body.find(b'item') != -1 and request.body.find(b'action') != -1:
            body = json.loads(request.body)
        if body['action'] == action:
            item = body['item']
            reason = body['reason']
            if reason == "":
                reason = "none"
            target_item_query = Product.objects.filter(name=item)
            target_item = target_item_query[0]
            target_taginfo = TagInfo.objects.filter(product=target_item)
            if len(target_taginfo) == 1:
                target_taginfo.delete()

                TagInfo.objects.create(product=target_item, tag=Tag.objects.filter(name=tag_name)[0], reason_added=reason)
                
                response = {
                    'status': 1,
                    'message': response_msg,
                    'item': body['item']
                }
    return response


@permission_required("store.delete_taginfo", login_url="/store/login")
def approve_item(request):
    response = swap_tag_helper(request=request, action="approve", tag_name="A")
    return JsonResponse(response)


@permission_required("store.delete_taginfo", login_url="/store/login")
def kick_back_item(request):
    response = swap_tag_helper(request=request, action="kick-back", tag_name="K")
    return JsonResponse(response)


@permission_required("store.delete_taginfo", login_url="/store/login")
def deny_item(request):
    response = swap_tag_helper(request=request, action="deny", tag_name="D")
    return JsonResponse(response)


@permission_required("store.change_product", login_url="/store/login")
def sell_item(request):
    response = {
        'status': 0,
        'message': 'ERROR: database not updated, something went wrong.'
    }
    if request.method == "POST":
        if request.body.find(b'item') != -1 and request.body.find(b'action') != -1:
            body = json.loads(request.body)
        if body['action'] == "sell" and body['price']:
            item = body['item']
            sold_price = float(body['price'])
            target_item_query = Product.objects.filter(name=item)
            target_item = target_item_query[0]
            target_taginfo = TagInfo.objects.filter(product=target_item)
            if len(target_taginfo) == 1:
                target_taginfo.delete()
                target_item.sold_price = sold_price
                TagInfo.objects.create(product=target_item, tag=Tag.objects.filter(name="S")[0], reason_added="none")
                response = {
                    'status': 1,
                    'message': "sold!",
                    'item': body['item']
                }
    return JsonResponse(response)


@permission_required("store.change_product", login_url="/store/login")
def submit_item(request):
    response = {
        'status': 0,
        'message': 'ERROR: database not updated, something went wrong.'
    }
    response = {
        'status': 0,
        'message': 'ERROR: database not updated, something went wrong.'
    }
    if request.method == "POST":
        if request.body.find(b'item') != -1 and request.body.find(b'action') != -1:
            body = json.loads(request.body)
        if body['action'] == "submit":
            item = body['item']
            price = body['price']
            description = body['description']
            target_item_query = Product.objects.filter(name=item)
            target_item = target_item_query[0]
            target_taginfo = TagInfo.objects.filter(product=target_item)
            if len(target_taginfo) == 1:
                target_taginfo.delete()
                target_item.list_price = price
                target_item.description = description
                TagInfo.objects.create(product=target_item, tag=Tag.objects.filter(name="P")[0], reason_added="none")
                response = {
                    'status': 1,
                    'message': "resubmitted",
                    'item': body['item']
                }
    return JsonResponse(response)





### user administration requests ###

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful, please log in.")
            return redirect("/store/login/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="store/register.html", context={"register_form":form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Logged in as {username}.")
                return redirect("/store/")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="store/login.html", context={"login_form":form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/store/")