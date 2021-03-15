from django.urls import path
from .views import IndexView
# from news.views import CategorySubscribeView

urlpatterns = [
    path('', IndexView.as_view()),
    # path('make_subscription/', CategorySubscribeView.as_view()),
]
