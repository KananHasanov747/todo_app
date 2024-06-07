from django.urls import path

from .views import ItemList, ItemCreate, ItemUpdate, ItemDelete

app_name = "todo"
urlpatterns = [
    path("", ItemList.as_view(), name="list"),
    path("create/", ItemCreate.as_view(), name="create"),
    path("update/<int:pk>/", ItemUpdate.as_view(), name="update"),
    path("delete/<int:pk>/", ItemDelete.as_view(), name="delete"),
]
