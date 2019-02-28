from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('', views.demand_list, name='demand_list'),
	path('demand/<int:id_demand>/', views.demand_detail, name='demand_detail'),
	path('demand/new/', views.demand_new, name='demand_new'),
	path('demand/<int:id_demand>/edit/', views.demand_edit, name='demand_edit'),
	path('demand/<id_demand>/remove/', views.demand_remove, name='demand_remove'),
	path('demand/<id_demand>/position_new', views.position_new, name='position_new'),
	path('demand/<id_demand>/position_edit/<id_position>/', views.position_edit, name='position_edit'),
	path('demand/<id_demand>/position_remove/<id_position>/', views.position_remove, name='position_remove'),
	path('demand/<id_demand>/create_pdf/', views.create_pdf, name='create_pdf'),
	path('non', views.non, name='non'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)