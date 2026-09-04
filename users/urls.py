from django.urls import path
from . import views




urlpatterns = [
    path('', views.guest_page, name='guestpage'), # Домка
    path('home', views.home_page, name='userhome'),

    path('create-primary-user', views.create_primary_user, name='create-primary-user'),
    path('set-password/<uuid:token>', views.set_password_view, name='password'),

    path('login/', views.login_page, name='loginpage'),
    path('logout/', views.logout_user, name='logout'),

    path('contracts/', views.contract_page, name='contracts'), # Контракты юзера - СПИСОК
    path('create-contract/', views.create_contract, name='contractform'),

    path('companies/', views.company_page, name='companies'),
    path('company-create', views.create_company, name='companyform'),

    path('tickets/', views.ticket_page, name='tickets'),  # Тикеты юзера - СПИСОК
    path('create-ticket/', views.create_ticket, name='supportticketform'),

    # path('applications/', views.application_page, name='applicationslist'),
    # path('application<>')
]
