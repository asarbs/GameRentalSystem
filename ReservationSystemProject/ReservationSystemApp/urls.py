from django.conf.urls import url


from . import views



urlpatterns = [
    url("NewClient/", views.NewClientView.as_view(), name="NewClient"),
    url("ClientDetails/(?P<pk>\d+)/", views.ClientDetails.as_view(), name="ClientDetails"),
    url("NewGame/", views.NewGameView.as_view(), name="NewGame"),
    url("GameList/", views.GameList.as_view(), name="GamesList"),
    url("GameDetails/(?P<pk>\d+)/", views.GameDetails.as_view(), name="GameDetails")
    ]