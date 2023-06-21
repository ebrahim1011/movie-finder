from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.conf import settings

from .forms import QueryForm, CheckForm, UserAdminCreationForm, LoginForm
from .utils import imdb, link_mink
from .models import Favorite


User = get_user_model()


class IndexView(ListView):
    template_name = 'filink/index.html'
    list_link = []
    context_object_name = list_link

    def get(self, request):
        fav_list = Favorite.objects.filter(auth=request.user.id)
        fav_list = fav_list.values_list('link', flat=True)
        list_session = self.request.session.get('list')
        imdb_session = self.request.session.get('imdb')
        form = QueryForm()
        check_form = CheckForm()
        return render(request, self.template_name, {'query_form': form, 'check_form': check_form,
                                                    "list": list_session, "imdb": imdb_session, "favorite": fav_list})

    def post(self, request):
        list_session = self.request.session.get('list')
        imdb_session = self.request.session.get('imdb')
        form = QueryForm(request.POST)
        check_form = CheckForm(request.POST)
        fav_list = Favorite.objects.filter(auth=request.user.id)
        fav_list = fav_list.values_list('link', flat=True)
        if check_form.is_valid():
            user_email = check_form.cleaned_data['email']
            request.session['email'] = user_email

            try:
                user = User.objects.filter(email=user_email).first()
            except:
                user = None

            if user:
                return HttpResponseRedirect('/loginuser')
            else:
                return HttpResponseRedirect('/registeruser')

        if form.is_valid():
            query = form.cleaned_data['query']
            fav_list = Favorite.objects.filter(auth=request.user.id)
            fav_list = fav_list.values_list('link', flat=True)
            self.list_link = link_mink(query)
            request.session['list'] = self.list_link
            imdb_list = imdb(query)
            request.session['imdb'] = imdb_list
            return render(request, self.template_name, {"query_form": form, "list": self.list_link,
                                                        "imdb": imdb_list, "favorite": fav_list})

        if request.method == 'POST':
            if "link" in request.POST:
                if not request.user.is_authenticated:
                    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
                fav = Favorite.objects.create(title=request.POST.get(
                    'title'), link=request.POST.get('link'), auth=request.user)
                fav_list = Favorite.objects.filter(auth=request.user.id)
                fav_list = fav_list.values_list('link', flat=True)
                fav.save()
                return render(request, self.template_name, {'query_form': form, 'check_form': check_form,
                                                            "list": list_session, "imdb": imdb_session, "favorite": fav_list})

            elif "delete" in request.POST:

                Favorite.objects.filter(link=request.POST['delete']).delete()
                fav_list = Favorite.objects.filter(auth=request.user.id)
                fav_list = fav_list.values_list('link', flat=True)
                return render(request, self.template_name, {'query_form': form, 'check_form': check_form,
                                                            "list": list_session, "imdb": imdb_session, "favorite": fav_list})

        return render(request, self.template_name, {'query_form': form, 'check_form': check_form,
                                                    "list": list_session, "imdb": imdb_session, "favorite": fav_list})


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'filink/login.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.session.get('email')
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['username'] = self.request.session.get('email')
        return initial

    def form_valid(self, form):
        valid = super().form_valid(form)
        user = form.get_user()
        login(self.request, user)
        return valid

    def form_invalid(self, form):
        return super().form_invalid(form)


class RegisterView(FormView):
    form_class = UserAdminCreationForm
    template_name = "filink/register.html"
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.session.get('email')
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.session.get('email')
        return initial

    def form_valid(self, form):
        valid = super().form_valid(form)

        form.save()
        user = form.save()
        login(self.request, user)
        return valid

    def form_invalid(self, form):
        return super().form_invalid(form)


class FavoriteView(ListView):
    template_name = 'filink/favorite.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        fav_list = Favorite.objects.filter(auth=request.user.id)
        return render(request, self.template_name, {"list": fav_list, })


def logout_view(request):
    logout(request)
    return redirect('/')
