from django.contrib.auth import logout, login, authenticate
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfilForm, CustomUserCreationForm
from .models import Profil
from .kod import generate_verification_code
from django.contrib import messages


@login_required
def profil(request):
    profil = Profil.objects.filter(user=request.user).first()
    return render(request, 'profil.html', {'profil': profil})


@login_required
def tahrirlash(request):
    try:
        profil = Profil.objects.filter(user=request.user).first()
    except Profil.DoesNotExist:
        messages.error(request, "Profil topilmadi")
        return

    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil muvaffaqiyatli yangilandi.")
            return redirect('profil:profil')
        else:
            messages.error(request, "Profilni yangilashda xatolik yuz berdi.")
    else:
        form = ProfilForm(instance=profil)

    return render(request, 'tahrirlash.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            kod = generate_verification_code()
            profil = Profil.objects.create(user=user, tasdiqla_kod=kod)

            if user.email:
                print(f"email uchun kod: {kod}")
                # send_mail(
                #     'Tasdiqlash kodi',
                #     f'Sizning tasdiqlash kodingiz: {kod}',
                #     'baxshilloyevferuz23@gmail.com',
                #     [user.email],
                #     fail_silently=False
                # )
                messages.success(request, "Tasdiqlash kodi emailingizga yuborildi.")
            elif profil.telefon:
                print(f"Telefon uchun kod: {kod}")
                messages.success(request, "Tasdiqlash kodi telefoningizga yuborildi .")
            else:
                print(kod)
                messages.warning(request, "Tasdiqlash kodi yuborilmadi: email yoki telefon topilmadi.")

            return redirect('profil:verify')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def send_code(user_email, code):
    subject = 'Tasdiqlash kodi'
    message = f"Sizning tasdiqlash kodingiz: {code}"
    from_email = 'baxshilloyevferuz23@gmail.com'
    send_mail(subject, message, from_email, [user_email])


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            code = generate_verification_code()
            profil = Profil.objects.filter(user=user).first()
            profil.tasdiqla_kod = code
            profil.save()

            print(code)
            # send_code(user.email, code)

            messages.success(request, 'Login muvaffaqiyatli. Tasdiqlash kodi yuborildi!')
            return redirect('profil:verify')

        else:
            messages.error(request, 'Login yoki parol noto‘g‘ri!')

    return render(request, 'login.html')


def verify_view(request):
    if request.method == 'POST':
        kod = request.POST.get('kod')
        profil = Profil.objects.filter(user=request.user).order_by('-kod_vaqt').first()
        print(profil.tasdiqla_kod)
        print(profil.kod_vaqt)
        if profil.tasdiqla_kod == kod:
            messages.success(request, "Tasdiqlash muvaffaqiyatli.")
            return redirect('profil:profil')
        else:
            messages.error(request, "Kod noto‘g‘ri.")
    return render(request, 'verify.html')


def logout_view(request):
    logout(request)
    return redirect('profil:login')
