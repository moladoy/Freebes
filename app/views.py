from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DeleteView
from app.form import ContactForm, LoginForm, RegisterForm
from app.models import Product, User, Contact


def index(request):
    return render(request, 'app/index.html')


def about(request):
    return render(request,'app/about.html')


def contact_view(request):
    if request.method == "Post":
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        text = request.POST.get('text')
        contact.name = name
        contact.email = email
        contact.text = text
        contact.save()
        return render(request, 'app/succes.html')
    return render(request, 'app/contact.html')


def single_post(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    context = {
        'product': product
    }
    return render(request, 'app/single-post.html', context)


def blog(request):
    products = Product.objects.order_by('-id')
    # product = products.objects.all()
    context = {
        'products':products,
        # 'items':product
    }
    return render(request, 'app/blog.html', context)


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('index')

    return render(request, 'app/login.html', {'form':form})


def logout_view(request):
    logout(request)
    return render(request, 'app/logout.html')


class blogPage(ListView):
    template_name = 'app/blog.html'
    model = Product
    queryset = Product.objects.all()
    context_object_name = 'products'


def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('index')
    context = {
        'form': form
    }
    return render(request, 'app/register.html', context)


class BlogSearchView(ListView):
    template_name = 'app/blog.html'
    model = Product
    queryset = Product.objects.all()
    context_object_name = 'products'

    def get_queryset(self):
        title = self.request.GET.get('title')
        if title:
            return Product.objects.filter(title__icontains=title)


class Register(generic.CreateView):
    from_class = UserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'app/register.html'


class UpdateBlogView(LoginRequiredMixin, UserPassesTestMixin,  UpdateView):
    model = Product
    fields = ('title', 'text', 'price',  'category', 'img', )
    template_name = 'update.html'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class DeleteBlogView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class CreateBlogView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'create.html'
    fields = ('title', 'text', 'price',  'category', 'img')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ShopPage(ListView):
    template_name = 'app/blog.html'
    model = Product
    queryset = Product.objects.all()
    context_object_name = 'products'
    # paginate_by = 3

    def get_queryset(self):
        title = self.request.GET.get('title')
        if title:
            return Product.objects.filter(title__icontains=title)
        return Product.objects.all()