from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Transactions
from .serializers import TransactionSerializer
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from .models import Bill, RecurringExpense, Budget
from .serializers import BillSerializer, RecurringExpenseSerializer, BudgetSerializer
import csv
from django.http import HttpResponse
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from openpyxl import Workbook


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@login_required
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
    
    
    
#Anamika
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@login_required
def notifications(request):
    user = request.user
    today = date.today()
    due_soon = Bill.objects.filter(
        user=user,
        paid=False,
        due_date__range=[today, today + timedelta(days=7)]
    )
    overdue = Bill.objects.filter(user=user, paid=False, due_date__lt=today)
    budgets = Budget.objects.filter(user=user)
    recurring = RecurringExpense.objects.filter(user=user)
    return Response({
        "due_soon_bills": BillSerializer(due_soon, many=True).data,
        "overdue_bills": BillSerializer(overdue, many=True).data,
        "budgets": BudgetSerializer(budgets, many=True).data,
        "recurring_expenses": RecurringExpenseSerializer(recurring, many=True).data,
    })   
    
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def budget_list(request):
    if request.method == 'GET':
        budgets = Budget.objects.filter(user=request.user)
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data)
    else:  
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def budget_detail(request, id):
    try:
        budget = Budget.objects.get(id=id, user=request.user)
    except Budget.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = BudgetSerializer(budget)
        return Response(serializer.data)
    else:  
        serializer = BudgetSerializer(budget, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_expenses_csv(request):
    transactions = Transactions.objects.filter(user=request.user, type=Transactions.CASH_OUT)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Description', 'Amount'])
    for tx in transactions:
        writer.writerow([tx.timestamp.date(), tx.description, tx.amount])
    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_budgets_csv(request):
    budgets = Budget.objects.filter(user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="budgets.csv"'
    writer = csv.writer(response)
    writer.writerow(['Category', 'Limit'])
    for b in budgets:
        writer.writerow([b.category, b.limit])
    return response   

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_expenses_pdf(request):
    transactions = Transactions.objects.filter(user=request.user, type=Transactions.CASH_OUT)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Expenses Report")
    p.setFont("Helvetica", 12)
    y = 780
    for tx in transactions:
        p.drawString(100, y, f"{tx.timestamp.date()}  {tx.description}  ${tx.amount}")
        y -= 20
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='expenses.pdf')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_budgets_pdf(request):
    budgets = Budget.objects.filter(user=request.user)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Budgets Report")
    p.setFont("Helvetica", 12)
    y = 780
    for b in budgets:
        p.drawString(100, y, f"{b.category}: ${b.limit}")
        y -= 20
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='budgets.pdf')   


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_expenses_excel(request):
    transactions = Transactions.objects.filter(user=request.user, type=Transactions.CASH_OUT)
    wb = Workbook()
    ws = wb.active
    ws.title = "Expenses"
    ws.append(["Date", "Description", "Amount"])
    for tx in transactions:
        ws.append([str(tx.timestamp.date()), tx.description, float(tx.amount)])
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="expenses.xlsx"'
    wb.save(response)
    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_budgets_excel(request):
    budgets = Budget.objects.filter(user=request.user)
    wb = Workbook()
    ws = wb.active
    ws.title = "Budgets"
    ws.append(["Category", "Limit"])
    for b in budgets:
        ws.append([b.category, float(b.limit)])
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="budgets.xlsx"'
    wb.save(response)
    return response