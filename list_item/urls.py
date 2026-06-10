from django.urls import path
from list_item.views import list_item_view, edit_view, new_list_item_view, done_view, all_done_view, delete_item_view, delete_all


app_name = 'list_item'

urlpatterns = [
    path('', list_item_view, name='list_item'),
    path('create_list/<int:pk>', new_list_item_view, name='new_list_item'),
    path('edit/<int:pk>', edit_view, name='edit'),
    path('done/', done_view, name='done'),
    path('all_done/', all_done_view, name='all_done'),
    path('delete/<int:pk>', delete_item_view, name='delete'),
    path('delete_all/', delete_all, name='delete_all'),
]