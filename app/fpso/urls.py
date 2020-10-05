from django.urls import path, include

from . import views

urlpatterns = [
    path('vessel/', include([
        path('', views.VesselListApiView.as_view() , name="vessel_list"),
        path('create/', views.VesselCreateApiView.as_view(), name="vessel_create"),
        path('<str:code>/equipments/', include([
            path('', views.VesselEquipmentListApiView.as_view(), name="vessel_equipment_list"),
            path('register/', views.EquipmentCreateApiView.as_view(), name="vessel_equipment_register"),
        ])),
    ])),
    
    path('equipments/', include([
        path('deactivate/', views.EquipmentStatusUpdateApiView.as_view(), name="equipment_deactivate"),
        path('activate/', views.EquipmentStatusUpdateApiView.as_view(), name="equipment_activate"),
    ])),
]