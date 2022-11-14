
import imp
from django.urls import path
from .views import DebtDetailsView

path('book-details', DebtDetailsView.as_view()),