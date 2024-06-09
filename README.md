# Todo App

### Project Structure

```
.
├── .gitignore
└── backend/
    ├── backend/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── db.sqlite3
    ├── manage.py
    └── todo/
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── forms.py
        ├── migrations/
        ├── models.py
        ├── static/
        │   └── todo/
        │       ├── base.css
        │       ├── create.css
        │       └── update.css
        ├── templates/
        │   └── todo/
        │       ├── base.html
        │       ├── create.html
        │       └── update.html
        ├── tests.py
        ├── urls.py
        └── views.py

```

---

## Process

### 0. Creating Python Virtual Environment (Optional)

- Create Python venv using the command `~$ python venv .venv`. Here, we've called our folder **.venv**.
- Activate it using the command `~$ source .venv/bin/activate`
- To deactivate it use the command `~$ deactivate`

### 1. Creating Project and App

- Create the project: `~$ django-admin startproject backend`
- Move into the root of the project: `~$ cd backend/`
- Create an app: `~$ python manage.py startapp todo`

### 2. Creating a Model

- Create a simple database model called **Item**

  ```python
  # todo/models.py

  from django.db import models


  class Item(models.Model):
      # Because we haven't added the 'id' field, Django automatically adds it as 'pk'
      title = models.CharField(max_length=30)
      text = models.CharField(max_length=500)
      date = models.DateTimeField("Date")

      def __str__(self):
          return f"{self.title}, {self.text}, {self.date}"
  ```

- Make migrations for creating file(s) under **_todo/migrations/_**: `~$ python manage.py makemigrations`
- Migrate by reading the migrations files and creating the actual **database** and **tables**
- Add the app to `INSTALLED_APPS` in `backend/settings.py`

  ```python
  # backend/settings.py
  ...
  INSTALLED_APPS = [
      ...
      "todo.apps.TodoConfig", # we can also remove '.apps.TodoConfig' if we keep 'TodoConfig' class unchanged
  ]
  ...
  ```

### 3. Creating views

- Create views for Todo App. Since there will be used CRUD operations, I've implemented something similar.<br />
  (note: instead of using the standard custom views, I used the class-based views for simplicity)

  ```python
  # todo/views.py

  from django.urls import reverse_lazy
  from django.views.generic import CreateView, UpdateView, DeleteView, ListView

  from .models import Item
  from .forms import ItemForm


  class ItemList(ListView):
      model = Item
      template_name = "todo/base.html"
      context_object_name = "post_list" # default 'object_list'


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

  ```

- This how it would like without using class-based views:

  ```python
  from django.shortcuts import render, redirect, get_object_or_404
  from .models import Item
  from .forms import ItemForm

  def item_list(request):
      post_list = Item.objects.all()
      return render(request, "todo/base.html", {"post_list": post_list})

  def item_create(request):
      if request.method == "POST":
          form = ItemForm(request.POST)
          if form.is_valid():
              form.save()
              return redirect("todo:list")
      else:
          form = ItemForm()
      return render(request, "todo/create.html", {"form": form})

  def item_update(request, pk):
      item = get_object_or_404(Item, pk=pk)
      if request.method == "POST":
          form = ItemForm(request.POST, instance=item)
          if form.is_valid():
              form.save()
              return redirect("todo:list")
      else:
          form = ItemForm(instance=item)
      return render(request, "todo/update.html", {"form": form})

  def item_delete(request, pk):
      item = get_object_or_404(Item, pk=pk)
      item.delete()
      return redirect("todo:list")
  ```

### 4. Connecting views to urls

```python
# todo/urls.py

from django.urls import path

from .views import ItemList, ItemCreate, ItemUpdate, ItemDelete

app_name = "todo" # settting the application namespace
urlpatterns = [
    # ex: /
    path("", ItemList.as_view(), name="list"),
    # ex: /create/
    path("create/", ItemCreate.as_view(), name="create"),
    # ex: /update/5/
    path("update/<int:pk>/", ItemUpdate.as_view(), name="update"), # 'pk' here is 'id'
    # ex: /delete/5/
    path("delete/<int:pk>/", ItemDelete.as_view(), name="delete"), # 'pk' here is 'id'
]

# from .views import item_list, item_create, item_update, item_delete
#
# urlpatterns = [
#     path("", item_list, name="list"),
#     path("create/", item_create, name="create"),
#     path("update/<int:pk>/", item_update, name="update"),
#     path("delete/<int:pk>/", item_delete, name="delete"),
# ]
```

### 5. Creating a form for HTML

Create a form class which applies three fields, like our Model.

```python
# todo/forms.py

from django import forms

from .models import Item

class ItemForm(forms.ModelForm):
  class Meta:
      model = Item
      fields = ["title", "text", "date"]
      # by default date's type is equal to 'datetime',
      # so in order to modify it we use argument 'widgets'
      widgets = {
          'date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
      }
```
