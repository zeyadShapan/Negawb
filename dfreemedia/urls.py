"""dfreemedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from categories import views as category_views
from django.conf.urls.static import static
from django.conf import settings
from users import views as users_views
from social import views as social_views
from production import views as production_views
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from categories import sitemaps
handler404 = production_views.handler404
handler500 = production_views.handler500


sitemaps = {
    'static': sitemaps.StaticViewSitemap,
    'post': sitemaps.PostSitemap,
    'people': sitemaps.PeopleSitemap,
    'feedback': sitemaps.FeedbackSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    # PWA
    path('', include('pwa.urls')),
    # Allauth
    path('accounts/', include('allauth.urls')),

    # Categories
    path('', category_views.home, name='home'),
    path('followed_posts/', category_views.followed_posts, name='followed_posts'),
    path('followed/', category_views.followed, name='followed'),
    # Chat
    path('chat/', social_views.chat, name='chat'),
    # production
    path('about/', production_views.About.as_view(), name='about'),
    path('faq/', production_views.Faq.as_view(), name='faq'),
    path('feedback/', production_views.feedback, name='feedback'),
    path('termsandconditions/', production_views.TermsAndConditions.as_view(),
         name='termsandconditions'),
    path('privacypolicy/', production_views.PrivacyPolicy.as_view(),
         name='privacypolicy'),
    path('cookiepolicy/', production_views.CookiePolicy.as_view(), name='cookiepolicy'),
    
    # Includes
    path('category/', include('categories.urls'), name='category'),
    path('comments/', include('comments.urls'), name='comments'),
    path('user/', include('userpage.urls'), name='userpage'),
    path('people/', include('people.urls'), name='people'),
    path('social/', include('social.urls'), name='social'),
    path('production/', include('production.urls'), name='production'),
    # AUTH
    path('signup/', users_views.signupuser, name='signupuser'),
    path('logout/', users_views.logoutuser, name='logoutuser'),
    path('login/', users_views.loginuser, name='loginuser'),
    path('activate/<uidb64>/<token>/',
         users_views.VertificationView.as_view(), name='activate'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('set_email_and_phone', users_views.set_email_and_phone,
         name="set_email_and_phone"),
    path('send_email_code', users_views.send_email_code, name="send_email_code"),
    path('confirm_email', users_views.confirm_email, name="confirm_email"),
    path('send_phone_code', users_views.send_phone_code, name="send_phone_code"),
    path('confirm_phone', users_views.confirm_phone, name="confirm_phone"),
    # Web-Push
    path('webpush/', include('webpush.urls')),
    # Menifest
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
