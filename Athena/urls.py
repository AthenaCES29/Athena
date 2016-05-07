from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from Promachos import views as views
from Promachos import APImobile as mobile

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.login),
    url(r'^home$', views.home),
    url(r'^login/$', views.login),
    url(r'^aluno/$', views.aluno),
    url(r'^logout/$', views.logout),
    url(r'^perfil/$', views.perfil),
    url(r'^professor/$', views.professor),
    url(r'^cadastro/$', views.register_user),
    url(r'^aluno/aluno_turmas/$', views.aluno_turmas),
    url(r'^prof_ativ/(?P<id_ativ>[0-9]+)/$', views.prof_ativ),
    url(r'^aluno/aluno_ativ/(?P<ativ_id>[0-9]+)/$', views.aluno_ativ),
    url(r'^Mlogin/$', mobile.login),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
