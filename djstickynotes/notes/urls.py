# urls.py
from django.urls import path
from .views import (
    stickynote_list,
    stickynote_detail,
    stickynote_create,
    stickynote_update,
    stickynote_delete,
)

urlpatterns = [
    path('', stickynote_list, name='stickynote_list'),
    path('<int:pk>/', stickynote_detail, name='stickynote_detail'),
    path('new/', stickynote_create, name='stickynote_create'),
    path('<int:pk>/edit/', stickynote_update, name='stickynote_update'),
    path('<int:pk>/delete/', stickynote_delete, name='stickynote_delete'),
]
