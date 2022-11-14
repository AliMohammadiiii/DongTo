# import viewsets
from itertools import count
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# import local data
from .serializers import DebtSerializer
from .models import debt


class DebtViewSet(viewsets.ModelViewSet):
    # define queryset
    # permission_classes = (AllowAny,)
    queryset = debt.objects.all()
    # specify serializer to be used
    serializer_class = DebtSerializer


class MyDebtList(APIView):

    # permission_classes = (AllowAny,)
    def get(self, request):
        user = self.request.user
        debt_list = debt.objects.filter(debtor=user).order_by('creditor')
        list_debt = []
        for debt_item in debt_list:
            if not debt_item.is_checkouted:
                debt_temp = [debt_item.creditor.id, 0]
                list_debt.append(debt_temp)
        debt_sum = 0
        for debt_item in debt_list:
            if not debt_item.is_checkouted:
                for i in list_debt:
                    if i[0] == debt_item.creditor.id:
                        i[1] += debt_item.price
                debt_sum += debt_item.price
        debtDict = {i[0]: i[1] for i in list_debt}
        return JsonResponse({'data': debtDict, 'sum': debt_sum})



@api_view(['POST'])
# @permission_classes([AllowAny])
def CheckOutItem(request, pk):
    if request.method == 'POST':
        debt.objects.filter(id = pk).update(is_checkouted=True)
        debt_item = debt.objects.filter(id = pk)
        serializer = DebtSerializer(debt_item, many = True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# @permission_classes([AllowAny])
def CheckOutCreditor(request, pk):
    if request.method == 'POST':
        user = request.user
        debt.objects.filter(creditor = pk).filter(debtor = user).update(is_checkouted=True)
        debt_item = debt.objects.filter(creditor = pk).filter(debtor = user)
        serializer = DebtSerializer(debt_item, many = True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

