import uuid

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, RegistrationToken, Companies
from .forms import CreateTicketForm, PrimaryUserForm, SetPasswordForm, CreateContractForm, CreateCompanyForm


LOGIN_URL = 'loginpage'


def guest_page(request):
    return render(request, 'users/mainpage.html')

def login_page(request): #проверяет авторизован ли пользователь, если да то пропускает на главную страницу, если нет то открывает страницу авторизации
    page = 'login'
    if request.user.is_authenticated:
        return redirect('userhome')
    if request.method == 'POST':
        uslog = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, login=uslog, password=password)
        if user is not None:
            login(request, user)
            return redirect('userhome')
        else: # если нет то ошибка
            messages.error(request, 'Неверный логин или пароль')
    context = {'page': page}
    return render(request, 'users/loginpage.html', context)

def create_primary_user(request): # создание первичной заявки на консультацию на открытие эквайринга
    if request.method == 'POST':
        form = PrimaryUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Заявка ещё не аккаунт с логином/паролем — генерируем
            # уникальный технический login, иначе вторая заявка падает
            # с IntegrityError (login у модели User обязателен и unique).
            user.login = f"lead-{uuid.uuid4()}"
            user.set_unusable_password()
            user.save()
            messages.success(request, 'Заявка отправлена, мы свяжемся с вами')
            return redirect('guestpage')
    else:
        form = PrimaryUserForm()

    return render(request, 'users/mainpage.html', {'form': form})

def set_password_view(request, token): # страница создания аккаунта (логин и пароль)
    registration_token = get_object_or_404(RegistrationToken, token=token)
    if not registration_token.is_valid():
        messages.error(request, 'Ссылка недействительна или истёк срок её действия')
        return redirect(LOGIN_URL)
    if request.method == 'POST':
        form = SetPasswordForm(registration_token.user, request.POST)
        if form.is_valid():
            form.save()
            registration_token.used = True
            registration_token.save()
            login(request, registration_token.user)
            return redirect('userhome')
    else:
        form = SetPasswordForm(registration_token.user)
    return render(request, "users/passwordform.html", {'form': form})


@login_required(login_url=LOGIN_URL)
def home_page(request):
    return render(request, 'users/userhome.html')

@login_required(login_url=LOGIN_URL)
def logout_user(request):
    logout(request)
    return redirect('guestpage') # выходит из аккаунта


@login_required(login_url=LOGIN_URL)
def contract_page(request):
    return render(request, 'users/contracts.html') # страница контрактов

@login_required(login_url=LOGIN_URL)
def create_contract(request):
    if request.method == 'POST':
        form = CreateContractForm(request.POST or None, user=request.user)
        if form.is_valid():
            form.save()
        return redirect('contracts')
    else:
        form = CreateContractForm(user=request.user)
    return render(request, 'users/contractform.html', {"form": form})


@login_required(login_url=LOGIN_URL)
def company_page(request):
    return render(request, 'users/companies.html')

@login_required(login_url=LOGIN_URL)
def create_company(request):
    if request.method == 'POST':
        form = CreateCompanyForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('companies')
    else:
        form = CreateCompanyForm()
    return render(request, 'users/companyform.html', {"form": form})


@login_required(login_url=LOGIN_URL)
def ticket_page(request):
    return render(request, 'users/tickets.html')

@login_required(login_url=LOGIN_URL)
def create_ticket(request):# создает тикет с данными из формы contract description
    if request.method == 'POST':
        form = CreateTicketForm(request.POST or None, user=request.user)
        if form.is_valid():
            form.save()
        return redirect('tickets')
    else:
        form = CreateTicketForm(user=request.user)

    return render(request, 'users/supticketform.html', {'form': form})

@login_required(login_url=LOGIN_URL)
def applications_list(request):
    return render(request, 'users/applicationslist.html')

@login_required(login_url=LOGIN_URL)
def application_page(request):
    return render(request, 'users/applications.html')

@login_required(login_url=LOGIN_URL)
def create_application(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заявка создана')
            form = CreateTicketForm()
    else:
        form = CreateTicketForm()

    return render(request, 'users/applicationform.html', {'form': form})
