from django.urls import path
from . import views

urlpatterns = [
    path('', views.support_page, name='supportpage'),
    path('primary-user-check/<int:id>/', views.primary_user_check, name='primary-user-check'),
    path('company-list/', views.companies_page, name='companypage'),
    path('company-check/<uuid:id>/', views.company_check, name='company-check'),
    path('ticket-list/', views.tickets_page, name='ticketpage'),
    path('ticket-check/<int:id>/', views.ticket_check, name='ticket-check'),
    path('contracts/', views.contracts_page, name='contractspage'),
    path('contract-check', views.contract_check, name='contract-check'),
]