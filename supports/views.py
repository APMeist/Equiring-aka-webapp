from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages


from .forms import CheckTicketForm, PrimaryUserCheckForm, CheckCompanyForm, CheckContractForm
from .models import SupporTicket

from users.models import Contracts, User, Companies


# Эта панель — внутренний инструмент поддержки/модерации, доступ только
# сотрудникам (is_staff=True), иначе любой посетитель мог бы одобрять
# заявки, компании, договоры и тикеты.
@staff_member_required(login_url='loginpage')
def support_page(request):
    return render(request, 'supports/supportpage.html')


@staff_member_required(login_url='loginpage')
def primary_user_check(request, id):

    primary_user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = PrimaryUserCheckForm(request.POST, instance=primary_user)

        if form.is_valid():
            form.save()
            return redirect('supportpage')

    else:
        form = PrimaryUserCheckForm(instance=primary_user)

    context = {'form': form}
    return render(request, 'supports/updateticketform.html', context)


@staff_member_required(login_url='loginpage')
def companies_page(request):
    return render(request, 'supports/companylist.html')

@staff_member_required(login_url='loginpage')
def company_check(request, id):

    company = get_object_or_404(Companies, id=id)

    if request.method == 'POST':

        form = CheckCompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('companypage')

    else:
        form = CheckCompanyForm(instance=company)

    context = {'form': form}
    return render(request, 'supports/updateticketform.html', context)


@staff_member_required(login_url='loginpage')
def tickets_page(request):
    return render(request, 'supports/ticketlist.html')

@staff_member_required(login_url='loginpage')
def ticket_check(request, id):  # изменяет статус тикета

    support_ticket = get_object_or_404(SupporTicket, id=id)

    if request.method == "POST":
        form = CheckTicketForm(request.POST, instance=support_ticket)

        if form.is_valid():
            form.save()
            return redirect('ticketpage')
    else:
        form = CheckTicketForm(instance=support_ticket)

    context = {'form': form}
    return render(request, 'supports/updateticketform.html', context)


@staff_member_required(login_url='loginpage')
def contracts_page(request):
    return render(request, 'supports/contractlist.html')

@staff_member_required(login_url='loginpage')
def contract_check(request):

        contract = get_object_or_404(Contracts, id=request.POST.get('id'))

        if request.method == 'POST':

            form = CheckContractForm(request.POST, instance=contract)
            if form.is_valid():
                form.save()
                return redirect('contractspage')

        else:
            form = CheckContractForm(instance=contract)

        context = {'form': form}
        return render(request, 'supports/updateticketform.html', context)