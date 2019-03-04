from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.demand_list, name='demand_list'),
	path('<int:id_demand>/', views.demand_detail, name='demand_detail'),
	path('new/', views.demand_new, name='demand_new'),
	path('<int:id_demand>/edit/', views.demand_edit, name='demand_edit'),
	path('<id_demand>/remove/', views.demand_remove, name='demand_remove'),
	path('<id_demand>/position_new', views.position_new, name='position_new'),
	path('<id_demand>/position_edit/<id_position>/', views.position_edit, name='position_edit'),
	path('<id_demand>/position_remove/<id_position>/', views.position_remove, name='position_remove'),
	path('non', views.non, name='non'),
	path('<id_demand>/documents/', include('documents.urls'))
]
