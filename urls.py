
from django.urls import path
from . import views

app_name="ideas"
urlpatterns = [
    path('create/', views.create, name="create"),
     path('delete/<int:idea_id>', views.delete, name="delete"),
      path('edit/<int:idea_id>', views.edit, name="edit"),
       path('view/<int:idea_id>', views.view, name="view"),
        path('vote/<int:idea_id>', views.vote, name="vote"),
        path('comment/', views.comment, name="comment"),
        path('list/', views.IdeaList.as_view()),
        path('api/', views.IdeaApiList.as_view()),
        path('api/<int:pk>', views.IdeaApiDetail.as_view()),

    ]
