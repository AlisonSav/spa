from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import FormView, DetailView, UpdateView, ListView, CreateView, DeleteView
from django.views.generic.list import MultipleObjectMixin

from core import settings
from spa import tasks
from spa.forms import RegisterForm, ContactForm, CommentModelForm
from spa.models import Review, CustomUser, Comment


@method_decorator(cache_page(15), "get")
class IndexListView(ListView):
    """Start page where User can sign up/sign in and see all Reviews and Comments"""

    model = Review
    context_object_name = "reviews"
    template_name = "spa/index.html"
    paginate_by = 25

    @method_decorator(cache_page(15))
    def get(self, request, *args, **kwargs):
        return super(IndexListView, self).get(self, request, *args, **kwargs)

    def get_queryset(self):
        reviews = Review.objects.order_by("-created_on")
        return reviews


class RegisterFormView(FormView):
    """View for User registration"""

    template_name = "registration/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("spa:profile")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


def logout_view(request):
    logout(request)
    return redirect("spa:index")


class UserProfile(LoginRequiredMixin, DetailView):
    """View with logged user's information. Logged user can modify his account information"""

    model = CustomUser
    template_name = "registration/profile.html"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """View for updating user's information"""

    model = CustomUser
    fields = ["avatar", "first_name", "last_name", "email"]
    template_name = "registration/update_profile.html"
    success_url = reverse_lazy("spa:profile")
    success_message = "Profile updated"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class AuthorListView(ListView):
    """View with all registered Users"""

    model = CustomUser
    context_object_name = "author"
    template_name = "spa/author_list.html"
    paginate_by = 20

    def get_queryset(self):
        return CustomUser.objects.all()


class AuthorDetailView(DetailView):
    """View with author's detail for any users"""

    model = CustomUser
    context_object_name = "author"
    template_name = "spa/author_detail.html"


class ReviewCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """View for crating review by logged user. Guest can only read and create comments"""

    model = Review
    fields = ["author", "text", "file"]
    template_name = "spa/review_create.html"
    success_message = "Review created"

    def form_valid(self, form):
        review_object = form.save(commit=False)
        review_object.author = self.request.user
        review_object.save()
        review_path = f"http://127.0.0.1:8000/review/{review_object.id}"
        send_mail(
            "New post!",
            loader.render_to_string(
                "spa/new_review_email.html",
                {"author": review_object.author, "text": review_object.text, "review_path": review_path},
            ),
            settings.NOREPLY_EMAIL,
            ["admin@a.com"],
            fail_silently=False,
        )
        return super().form_valid(form)


class ReviewDetailView(DetailView, MultipleObjectMixin):
    """View with Review details"""

    model = Review
    template_name = "spa/review_detail.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        comments_list = Comment.objects.filter(review=self.object.id)
        context = super(ReviewDetailView, self).get_context_data(object_list=comments_list, **kwargs)
        paginator = Paginator(comments_list, 10)
        page = self.request.GET.get("page")
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        context["comments"] = comments
        return context


class ReviewUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """View for updating Review by user-owner"""

    model = Review
    fields = ["author", "text", "file"]
    template_name = "spa/review_update.html"
    success_message = "Post updated"


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    """View for review deleting"""

    model = Review
    success_url = reverse_lazy("spa:index")
    success_message = "Review deleted"

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user)


def comment_create(request, pk):
    """View for creating comment on Review details"""

    review = get_object_or_404(Review, pk=pk)
    user = request.user
    if request.method == "POST":
        form = CommentModelForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                review_id=pk,
                author=form.cleaned_data["author"],
                comment_text=form.cleaned_data["comment_text"],
            )
        return redirect("spa:index")
    else:
        if user.is_authenticated:
            form = CommentModelForm(initial={"author": request.user.username})
        else:
            form = CommentModelForm()
    return render(request, "spa/create_comment.html", {"form": form, "review": review})


def contact_us(request):
    """Contact form"""

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            tasks.post_email(
                form.cleaned_data.get("subject"),
                form.cleaned_data.get("message"),
                [form.cleaned_data.get("from_email")],
            )
            return redirect(reverse("spa:index"))
    else:
        form = ContactForm()
    return render(request, "spa/partial_contact_create.html", {"form": form})
