from django.conf.urls import url


from . import views



urlpatterns = [
    url("NewClient/", views.NewClientView.as_view(), name="NewClient"),
    url("NewGame/", views.NewGameView.as_view(), name="NewGame")
    ]