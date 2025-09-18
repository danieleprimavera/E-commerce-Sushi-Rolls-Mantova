from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.rolls, name='home'),
    path('contattaci', views.contattaci, name='contattaci'),
    path('carrello/', views.carrello, name='carrello'),
    path('aggiungi/<int:roll_id>/', views.aggiungi_al_carrello, name='aggiungi_al_carrello'),
    path('carrello/<int:roll_id>/<str:action>/', views.aggiorna_carrello, name='aggiorna_carrello'),
    path('checkout/', views.checkout, name='checkout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path("search/", views.search, name="search"),
    path("add-to-cart/<int:roll_id>/", views.add_to_cart, name="add_to_cart"),
]
