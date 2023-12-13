

from django.contrib import admin
from django.urls import path, include
from list_of_diseases import views
from rest_framework import routers
from rest_framework import permissions
from django.urls import path, include
# from drf_yasg import get_schema_view
# from drf_yasg import openapi

router = routers.DefaultRouter()



# schema_view = get_schema_view(
#    openapi.Info(
#       title="Snippets API",
#       default_version='v1',
#       description="Test description",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', views.DiseasesList),
    # path('disease/<int:id>/', views.GetDisease, name='disease_url'),
    # path('delete/<int:id>/', views.Delete, name='delete_url'),
    


    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),

    # для заболеваний (=услуг) 
    path(r'diseases/', views.get_diseases, name='diseases_list'),
    path(r'diseases/get_found_diseases/', views.get_found_diseases, name='get_found_diseases'),
    path(r'diseases/post/', views.post_disease, name='diseases_post'),
    path(r'diseases/<int:id>/', views.get_disease, name='disease_detail'),
    path(r'diseases/<int:id>/update/', views.put_disease, name='disease_put'),
    path(r'diseases/<int:id>/delete/', views.delete_disease,name='disease_delete'),
    path(r'diseases/<int:id>/add_disease_to_drug/', views.add_disease_to_drug, name='add_disease_to_drug'), # (post)

    # для препаратов (=заявок)
    path(r'drugs/', views.get_drugs, name='drugs_list'),
    path(r'drugs/<int:id>/', views.get_drug, name='drug_detail'),
    path(r'drugs/<int:id>/put/', views.update_drug, name='drug_put'),
    path(r'drugs/<int:id>/delete/', views.delete_drug,name='drug_delete'),
    path(r'drugs/delete_entered_drug/', views.delete_entered_drug,name='delete_entered_drug'),
    path(r'drugs/<int:id>/update_st_user/', views.drug_update_status_user,name='drug_update_status_user'),
    path(r'drugs/<int:id>/update_st_admin/', views.drug_update_status_admin,name='drug_update_status_admin'),
    path(r'drugs/<int:disease_id_r>/<int:drug_id_r>/delete_disease_from_drug/', views.delete_disease_from_drug, name='delete_disease_from_drug'),


    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path(r'register/', views.register, name="register"),
    path(r'login/',  views.login_view, name='login'),
    path(r'logout', views.logout_view, name='logout'),

]
