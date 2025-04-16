from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Transactions
from .serializers import TransactionSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def transaction_list(request):
    # Get the 'type' query parameter (optional)
    transaction_type = request.query_params.get('type', None) #Here type is a param that is passed in the request

    if request.method == "GET":
        # If 'type' is provided, filter by the specified type (cash_in or cash_out)
        if transaction_type:
            transactions = Transactions.objects.filter(user=request.user, type=transaction_type)
        else:
            # If no 'type' is specified, return all transactions for the user
            transactions = Transactions.objects.filter(user=request.user)

        # Serialize the filtered transactions
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        # Create a new transaction
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            # Associate the transaction with the logged-in user
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
