from django.conf.urls import url


from . import views



urlpatterns = [
    url("NewClient/", views.NewClientView.as_view(), name="NewClient"),
    url("ClientDetails/(?P<pk>\d+)/", views.ClientDetails.as_view(), name="ClientDetails"),
    url("ClientList/", views.ClientList.as_view(), name="ClientList"),
    url("ClientEdit/(?P<pk>\d+)/", views.ClientEdit.as_view(), name="ClientEdit"),
    url("DeleteClient/(?P<pk>\d+)/", views.DeleteClient, name="DeleteClient"),
    url("NewGame/", views.NewGameView.as_view(), name="NewGame"),
    url("GameList/", views.GameList.as_view(), name="GamesList"),
    url("GameUpdate/(?P<pk>\d+)/", views.GameEdit.as_view(), name="GameUpdate"),
    url("GameDetails/(?P<pk>\d+)/", views.GameDetails.as_view(), name="GameDetails"),
    url("NewGameCopy/", views.NewGameCopy, name="NewGameCopy"),
    url("DeleterGameCopy/(?P<pk>\d+)/", views.DeleteGamesCopy, name="DeleterGameCopy"),
    url("DeleteGame/(?P<pk>\d+)/", views.GameDelete, name="DeleteGame"),
    url("GameCopyDetails/(?P<pk>\d+)/", views.GameCopyDetails.as_view(), name="GameCopyDetails"),
    url("Rental/", views.Rental, name="Rental"),
    url("makeReturn/(?P<pk>\d+)/", views.makeReturn, name="makeReturn"),
    url("formReturn/", views.Return, name="Return"),
    url("GameCopyReturn/(?P<pk>\d+)/", views.GameCopyReturn, name="GameCopyReturn"),
    url("NewEvent/", views.NewEvent.as_view(), name="NewEvent"),
    url("EventDetails/(?P<pk>\d+)/", views.EventDetails.as_view(), name="EventDetails"),
    url("ListEvent", views.ListEvent.as_view(), name="ListEvent"),
    url("EventUpdate/(?P<pk>\d+)/", views.EventUpdate.as_view(), name="EventUpdate"),
    url("SelectEvent/", views.SelectEvent, name="SelectEvent"),
    url('^addUser$', views.addUser,  name="addOperator"),
    url('changePassword/', views.changePassword, name="changePassword"),
    url('operatorList/', views.OperatorList.as_view(), name="operatorList"),
    url('deactivateOperator/(?P<pk>\d+)/', views.DeactivateOperator, name="deactivateOperator"),
    url('activateOperator/(?P<pk>\d+)/', views.ActivateOperator, name="activateOperator"),
    url('statistics/', views.statistics, name='statistics'),
    url('RentalList/', views.RentalList.as_view(), name='RentalList'),
    url('AddPaymentCategories/', views.NewPaymentCategories.as_view(), name='AddPaymentCategories'),
    url('EditPaymentCategories/(?P<pk>\d+)/', views.UpdatePaymentCategories.as_view(), name='EditPaymentCategories'),
    url('PaymentCategories/', views.PaymentCategoriesList.as_view(), name='PaymentCategories')
    ]