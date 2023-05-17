from django.contrib import admin
from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='home'),
    path('create', views.article_create, name='create'),
    path('article/<int:id>/', views.article_details, name='details'),
    path('article/<int:id>/edit/', views.article_edit, name='edit'),
    path('article/<int:id>/delete/', views.article_delete, name='delete'),
#     new type of create
    path('article_new',views.article_new,name='article_new'),
    path('edit_new/<int:id>/',views.article_edit_new,name='edit_new'),

    path('comment/<int:id>/delete/',views.comment_delete,name='comment_delete'),
    path('comment_edit/<int:id>/',views.comment_edit,name='comment_edit')


]