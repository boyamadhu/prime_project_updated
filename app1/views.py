from django.shortcuts import render,redirect
from app1.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from random import randint

otp = None

#OTP Function
# def generate_otp(request):
#     global otp
#     otp = random.randint(1000, 9999)
#     return redirect('otp')

# def otp_verification(request):
#     global otp
#     if request.method == 'POST':
#         user_otp = request.POST.get('otp')
#         if user_otp == str(otp):
#             return HttpResponseRedirect(reverse('prime_home'))
#         else:
#             message = "Incorrect OTP. Please try again."
#     else:
#         message = None
#     return render(request, 'otp.html', {'message': message})


# Create your views here.
@login_required
def object(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO, 'PO':PO, 'username':username}
    return d


def register(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}

    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            NSUO=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            NSUO.set_password(password)
            NSUO.save()

            NSPO=pfd.save(commit=False)
            NSPO.username=NSUO
            NSPO.save()
            # un=request.POST['username']
            # pw=request.POST['password']
            # AO=authenticate(username=un,password=pw)
            # login(request,AO)
            # request.session['username']=un
            send_mail('Registering prime','Congrats You have successfully registered amazon prime', 
                      'boyamadhus9493@gmail.com',[NSUO.email],fail_silently=False)
            return HttpResponseRedirect(reverse('prime'))
            #return render(request, 'generate_otp.html')
        else:
            return HttpResponse('Not valid')

    return render(request,'register.html',d)

def user_login(request):
    if request.method=='POST':
        un=request.POST['email']
        pw=request.POST['password']
        AO=authenticate(username=un,password=pw)
        d = {'PO':un}
        if AO and AO.is_active:
            login(request,AO)
            request.session['username']=un
            
            return HttpResponseRedirect(reverse('prime_home'),d)
        else:
            return render(request,'user_login.html')

    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('prime'))

def prime(request):
    return render(request,'prime.html')

def dummy(request):
    return render(request,'dummy.html')

@login_required
def prime_home(request):
    d=object(request)
    return render(request,'prime_home.html',d)

def catagories(request):
    if request.session.get('username'):
        d=object(request)
        return render(request,'catagories.html',d)
    
    return render(request,'catagories.html')

def create_account(request):
    return render(request,'create_account.html')

def store(request):
    if request.session.get('username'):
        d=object(request)
        return render(request,'store.html',d)
    return render(request,'store.html')

def practice(request):
    return render(request,'practice.html')

@login_required
def update_password(request):
    if request.method=='POST':
        OP=request.POST['oldpass']
        NO=request.POST['newpass']
        if NO:
            if OP==NO:
                username=request.session.get('username')
                OB=User.objects.get(username=username)
                OB.set_password(NO)
                OB.save()

                send_mail(f'Hi {OB.username}','Thanks for visiting Amazon.com! Per your request, we have successfully changed your password.Visit Your Account at Amazon.com to view your orders, make changes to any order that hasnt yet entered the shipping process, update your subscriptions, and much more.Should you need to contact us for any reason, please know that we can give out order information only to the name and e-mail address associated with your account. Thanks again for shopping with us.', 
                      'boyamadhus9493@gmail.com',[OB.email],fail_silently=False)
                logout(request)
                return HttpResponseRedirect(reverse('prime'))
            else:
                return HttpResponse('password is not matched')
        else:
            return HttpResponse('please type password')
    return render(request,'update_password.html')

def generate_code():
    return str(randint(100000, 999999))


def forgot_password(request):
    if request.method == 'POST':
        un = request.POST['username']
        UO = User.objects.filter(username=un)
        if UO:
            UO = User.objects.get(username=un)
            verification_code = generate_code()
            UO.profile.verification_code = verification_code
            UO.profile.save()
            send_mail(
                'Password Reset Verification Code',
                f'Your verification code is {verification_code}',
                'from@example.com',  # Replace with your actual "from" email address
                [UO.email],
                fail_silently=False,
            )
            # Redirect to the verify_code page with the username as a URL parameter
            return redirect('verify_code', username=un)
        else:
            return HttpResponse('User is not available')
    return render(request, 'forgot_password.html')


def verify_code(request, username=None):
    if request.method == 'POST':
        un = request.POST.get('username', username)
        code = request.POST['code']
        pw = request.POST['newpass']
        rw = request.POST['repass']
        UO = User.objects.filter(username=un)
        if UO:
            UO = User.objects.get(username=un)
            if UO.profile.verification_code == code:
                if pw == rw:
                    UO.set_password(pw)
                    UO.profile.verification_code = ''  # Clear the code after successful reset
                    UO.profile.save()
                    UO.save()
                    # Redirect to a success page or login page
                    return redirect('user_login')
                else:
                    return HttpResponse('Passwords do not match')
            else:
                return HttpResponse('Invalid verification code')
        else:
            return HttpResponse('User is not available')
    # Render the verify code form with the username included
    return render(request, 'verify_code.html', {'username': username})


@login_required
def payment_page(request):
    if request.method == 'POST':
        # nm=request.POST['name']
        # ss=Profile.objects.get(username=nm)
        # ss['subscrption']=True
        # ss.save()
        UO=request.user.id
        Profile.objects.filter(username=UO).update(subscription=True)
        d=object(request)
        #return render(request,'prime_home.html',d)
        return HttpResponseRedirect(reverse('prime_home'))
        
    d=object(request)
    return render(request, 'payment_page.html',d)

@login_required
def profile_page(request):
    d=object(request)
    return render(request, 'profile_page.html',d)

@login_required
def rentals(request):
    d=object(request)
    return render(request, 'rentals.html',d)

# search result for movies
def display_movies(request):
    MO = Search.objects.all()
    d = {'MO' :MO}
    return render(request, 'display_movies.html', d)

def search_m(request):
    search_query = request.POST['search_m']
    MO = Search.objects.filter(movie_name__contains=search_query)
    d = {'MO' :MO, 'movie_name' : search_query}
    d.update(object(request))
    return render(request, 'display_movies.html', d)


# CHANNELS FUNCTIONS
def lionsgate(request):
    d=object(request)
    return render(request, 'channels/lionsgate.html',d)
def discovery(request):
    d=object(request)
    return render(request, 'channels/discovery.html',d)
def docubay(request):
    d=object(request)
    return render(request, 'channels/docubay.html',d)
def erosnow(request):
    d=object(request)
    return render(request, 'channels/erosnow.html',d)
def hoichoi(request):
    d=object(request)
    return render(request, 'channels/hoichoi.html',d)
def iwonder(request):
    d=object(request)
    return render(request, 'channels/iwonder.html',d)
def monoramax(request):
    d=object(request)
    return render(request, 'channels/monoramax.html',d)
def mubi(request):
    d=object(request)
    return render(request, 'channels/mubi.html',d)
def amc(request):
    d=object(request)
    return render(request, 'channels/amc.html',d)
def shortstv(request):
    d=object(request)
    return render(request, 'channels/shortstv.html',d)
def stingray(request):
    d=object(request)
    return render(request, 'channels/stingray.html',d)
def vrott(request):
    d=object(request)
    return render(request, 'channels/vrott.html',d)

# CATAGORIES FUNCTIONS
def drama_movies(request):
    catagorie = 'drama'
    MO = Search.objects.filter(category__contains=catagorie)
    d = {'MO' :MO, 'category' : catagorie}
    d.update(object(request))
    return render(request, 'catagories/drama.html',d)
def anime_movies(request):
    catagorie = 'anime'
    MO = Search.objects.filter(category__contains=catagorie)
    d = {'MO' :MO, 'category' : catagorie}
    d.update(object(request))
    return render(request, 'catagories/drama.html',d)
def action_movies(request):
    catagorie = 'action'
    MO = Search.objects.filter(category__contains=catagorie)
    d = {'MO' :MO, 'category' : catagorie}
    d.update(object(request))
    return render(request, 'catagories/drama.html',d)
def comedy_movies(request):
    catagorie = 'comedy'
    MO = Search.objects.filter(category__contains=catagorie)
    d = {'MO' :MO, 'category' : catagorie}
    d.update(object(request))
    return render(request, 'catagories/drama.html',d)
def documentary_movies(request):
    catagorie = 'documentary'
    MO = Search.objects.filter(category__contains=catagorie)
    d = {'MO' :MO, 'category' : catagorie}
    d.update(object(request))
    return render(request, 'catagories/drama.html',d)
# for adding movies
@login_required
def add_movie(request):
    if request.method == 'POST' and request.FILES:
        form = SearchForm(request.POST,request.FILES)
        movie = form.save(commit=False)
        movie.save()
        d=object(request)
        MO = Search.objects.all()
        d1 = {'MO' :MO}
        d.update(d1)
        return render(request,'display_movies.html',d)  # Redirect to a view that lists all movies
    else:
        form = SearchForm()
        d={'form':form}
        d.update(object(request))
    return render(request, 'add_movie.html', d)