from django.shortcuts import render
from .models import Expense

def home(request):
    data = Expense.objects.all()

    total = 0
    count = 0

    for x in data:
        total += x.amount
        count += 1

    if count > 0:
        prediction = total + 500
    else:
        prediction = 0

    budget = 5000
    remaining = budget - total

    return render(request, 'home.html', {
        'data': data,
        'prediction': prediction,
        'total': total,
        'remaining': remaining
    })