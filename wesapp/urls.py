from django.contrib import admin
from django.urls import path
from wesapp import views
from django.conf import settings
from django.conf.urls.static import static
from .views import AddPostView, DeletePostView, UpdatePostView, home, register, login_user, logout_user, about, footer, home01, subscription, profile, HomeView, ArticleDetail, feed, home_body, UpdatePostView, DeletePostView, news, contact, premium_access, like_post, AddCommentView, mypost, user_change_pass

admin.site.site_header = "Mehdi Alam"
admin.site.site_title = 'title'
admin.site.index_title = "Welcome!!"

urlpatterns = [
    path('base', home, name='home'),
    path('news/', news, name='news'),

    path('contact', contact, name='contact'),

    path('premium_access/', premium_access, name='premium_access'),
    path('', home01, name='home01'),
    path('w', home_body, name='home_body'),
    path('register/', register, name='register'),

    path('login_user', login_user, name="login_user"),
    path('logout_user', logout_user, name="logout_user"),
    path('about/', about, name="about"),
    path('footer/', footer, name="footer"),
    path('subscription/', subscription, name="subscription"),
    path('profile/', profile, name="profile"),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('articleDetail/<int:pk>', ArticleDetail.as_view(), name='articleDetail'),
    # path('feed/', feed, name='feed'),

    path('mypost/', mypost, name='mypost'),

    path('feed/', HomeView.as_view(), name='feed'),
    path('articleDetail/edit/<int:pk>',
         UpdatePostView.as_view(), name='update_post'),

    path('articleDetail/<int:pk>remove',
         DeletePostView.as_view(), name='delete_post'),
    path(r'^like/$', like_post, name="like_post"),

    path('articleDetail/<int:pk>/comment',
         AddCommentView.as_view(), name="add_comment"),

    path('changepass/', views.user_change_pass, name='changepass')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
