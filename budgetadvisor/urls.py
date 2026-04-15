from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from expenses.views import (
    welcome,
    register_user,
    login_user,
    logout_user,
    dashboard,
    add_expense,
    history,
    chart,
    edit_expense,
    delete_expense,
    download_pdf
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', welcome),

    path('register/', register_user),
    path('login/', login_user),
    path('logout/', logout_user),

    path('dashboard/', dashboard),
    path('add/', add_expense),
    path('history/', history),
    path('chart/', chart),

    path('edit/<int:id>/', edit_expense),
    path('delete/<int:id>/', delete_expense),

    path('pdf/', download_pdf),
]

urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATICFILES_DIRS[0]
)