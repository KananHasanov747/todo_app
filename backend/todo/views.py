from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from .models import Item
from .forms import ItemForm


class ItemList(ListView):
    model = Item
    template_name = "todo/base.html"
    context_object_name = "post_list"


class ItemCreate(CreateView):
    model = Item
    template_name = "todo/create.html"
    form_class = ItemForm
    success_url = reverse_lazy("todo:list")


class ItemUpdate(UpdateView):
    model = Item
    template_name = "todo/update.html"
    form_class = ItemForm
    success_url = reverse_lazy("todo:list")


class ItemDelete(DeleteView):
    model = Item
    success_url = reverse_lazy("todo:list")
