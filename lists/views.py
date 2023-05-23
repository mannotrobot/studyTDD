from django.shortcuts import redirect, render
from lists.models import Item, List



# Create your views here.
def home_page(request):
    """home page my app"""
    return render(request, 'home.html')


def view_list(request, list_id):
    """представления списка"""
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    """новый список"""
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')

def add_item(request, list_id):
    """добавить новый элемент в список"""
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
