"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),  # DRF browsable API
    path("api/users/", include("users.urls")),  # users API
]

# ==================================================================== #
# DEBUG 일때만 swagger, URL patterns 추가해서 사용
# ==================================================================== #

schema_view = get_schema_view(
    openapi.Info(
        title="Django Boilerplate (@msm9401) rest API",
        default_version="v1.0",
        description="Django Boilerplate (@msm9401) rest API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(name="msm9401", email="anstmdals94@gmail.com"),
        license=openapi.License(name="Private License"),
    ),
    public=True,
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
        re_path(r"__debug__/", include(debug_toolbar.urls)),
    ]

    settings.MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    SHOW_TOOLBAR_CALLBACK = True
