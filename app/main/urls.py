from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('cam', views.ImageRubbish_upload_view),
    path('ImageRubbishUpload', views.ImageRubbish_upload_view),
    path('ImageFaceUpload', views.ImageFace_upload_view),
    path('jup', views.jup),
    path('main', views.main),
    path('', views.main),
    path('team', views.team),
    path('mat', views.mat),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
