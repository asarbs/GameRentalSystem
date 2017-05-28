from django.conf.urls import url


from . import views



urlpatterns = [
    url("NewClient/", views.NewClientView.as_view(), name="NewClient"),
    url("ClientDetails/(?P<pk>\d+)/", views.ClientDetails.as_view(), name="ClientDetails"),
    url("NewGame/", views.NewGameView.as_view(), name="NewGame"),
    url("GameList/", views.GameList.as_view(), name="GamesList"),
    url("GameUpdate/(?P<pk>\d+)/", views.GameEdit.as_view(), name="GameUpdate"),
    url("GameDetails/(?P<pk>\d+)/", views.GameDetails.as_view(), name="GameDetails"),
    url("NewGameCopy/", views.NewGameCopy, name="NewGameCopy"),
    url("DeleterGameCopy/(?P<pk>\d+)/", views.DeleteGamesCopy, name="DeleterGameCopy"),
    url("DeleteGame/(?P<pk>\d+)/", views.GameDelete, name="DeleteGame")
    ]