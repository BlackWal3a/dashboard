from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingpage_view, name='landingpage'),
    path('aircraft/', views.overview_list, name='aircraft_list'),
    path('dashboard/', views.overview_list, name='dashboard'),
    path('suppliers/', views.suppliers_view, name='suppliers'),
    path('geography/', views.geo_view, name='geography'),
    path('timeline/',views.time_view, name='timeline'),
    path('aircrafts/', views.aircrafts_view, name='aircrafts'),
    path('sign-in/', views.signin_view, name='sign-in'),
    path('change-password/', views.change_password, name='change_password'),
    path('create-account/', views.createaccount_view, name='create_account'),
    path('rtl/', views.prevision_view, name='rtl'),
    path('profile/', views.profile_view, name='profile'),
    path('receive_data/', views.receive_data, name='receive_data'),
    path('receive_DeliveryOrders/', views.receive_deliveryorders, name='receive_DeliveryOrders'),
    path('receive_extchangerates/', views.receive_extchangerates, name='receive_extchangerates'),
    path('logout/', views.logout_view, name='logout'),
    path('forecasting/', views.forecasting_view, name='forecasting'),
    path('save_date/', views.save_date_view, name='save_date'),
    path('country_details/', views.country_details, name='country_details'),
    path('edit-notes/', views.edit_notes, name='edit_notes'),
    path('about/', views.about_view, name='about'),
    path('save_geo_date/', views.save_geo_date, name='save_geo_date'),
    path('save_supplier_date/', views.save_supplier_date, name='save_supplier_date'),
]
