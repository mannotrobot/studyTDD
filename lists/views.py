from django.shortcuts import redirect, render

from lists.models import List
from lists.forms import ItemForm, ExistingListItemForm


# Create your views here.
def home_page(request):
    """home page my app"""
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    """представления списка"""
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)

    if request.method == "POST":
        form = ExistingListItemForm(for_list=list_, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect(list_)

    return render(request, 'list.html', {'list': list_, 'form': form})


def new_list(request):
    """новый список"""
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})

