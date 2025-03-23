from django.urls import path
from .views import (
    IndexView,
    AboutView,
    ContactView,
    GalleryView,
    ManageTicketView,
    SignInView,
    SearchResultView,
    PaymentView,
    ManageTicketDetailView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('manageticket/', ManageTicketView.as_view(), name='manageticket'),
    path('manageticket/<str:pk>/', ManageTicketDetailView.as_view(), name='manageticket-detail'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('searchresult/', SearchResultView.as_view(), name='searchresult'),
    path('payment/', PaymentView.as_view(), name='payment'),
]