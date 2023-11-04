from rest_framework import generics
from .models import Account
from .serializers import AccountSerializer

class AccountView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer