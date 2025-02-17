from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.conf.urls.static import static
from django.conf import settings

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),
    path('auth/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
