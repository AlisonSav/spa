from django.urls import path, include

from spa import views

app_name = "spa"
urlpatterns = [
    path("", views.IndexListView.as_view(), name="index"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", views.RegisterFormView.as_view(), name="register"),
    path("accounts/profile/", views.UserProfile.as_view(), name="profile"),
    path("accounts/update_profile/", views.UpdateProfile.as_view(), name="update_profile"),
    path("author_list/", views.AuthorListView.as_view(), name="author_list"),
    path("author/<int:pk>", views.AuthorDetailView.as_view(), name="author_detail"),
    path("review_create/", views.ReviewCreateView.as_view(), name="review_create"),
    path("review/<int:pk>", views.ReviewDetailView.as_view(), name="review_detail"),
    path("review/<int:pk>/update/", views.ReviewUpdateView.as_view(), name="review_update"),
    path("review/<int:pk>/delete/", views.ReviewDeleteView.as_view(), name="review_delete"),
    path("review/<int:pk>/comment_create/", views.comment_create, name="comment_create"),
    path("contact_us/", views.contact_us, name="contact_us"),
]
