from django.contrib import admin
from django.urls import path
from expenses.views import welcome, dashboard, add_expense, history, delete_expense, chart, edit_expense, register_user, login_user, logout_user
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome),
    path('dashboard/', dashboard),
    path('add/', add_expense),
    path('history/', history),
    path('chart/', chart),
    path('edit/<int:id>/', edit_expense),
    path('delete/<int:id>/', delete_expense),
    path('register/', register_user),
    path('login/', login_user),
    path('logout/', logout_user),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])