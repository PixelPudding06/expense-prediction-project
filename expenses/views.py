from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from sklearn.linear_model import LinearRegression

def dashboard(request):
    data = Expense.objects.all().order_by('-date')

    total = sum(x.amount for x in data)

    amounts = [x.amount for x in data]
    months = [[i+1] for i in range(len(amounts))]

    if len(amounts) > 1:
        model = LinearRegression()
        model.fit(months, amounts)
        prediction = int(model.predict([[len(amounts)+1]])[0])

    elif len(amounts) == 1:
        prediction = amounts[0]

    else:
        prediction = 0

    remaining = 5000 - total

    labels = []
    values = []

    for x in data:
        labels.append(x.category)
        values.append(x.amount)

    return render(request, 'dashboard.html', {
        'data': data[:5],
        'total': total,
        'prediction': prediction,
        'remaining': remaining,
        'labels': labels,
        'values': values
    })

def add_expense(request):
    if request.method == "POST":
        Expense.objects.create(
            category=request.POST['category'],
            amount=request.POST['amount'],
            date=request.POST['date']
        )
        return redirect('/history/')

    return render(request, 'add_expense.html')


def history(request):
    data = Expense.objects.all().order_by('-date')
    return render(request, 'history.html', {'data': data})


def delete_expense(request, id):
    item = get_object_or_404(Expense, id=id)
    item.delete()
    return redirect('/history/')
def chart(request):
    data = Expense.objects.all()

    labels = []
    values = []

    for x in data:
        labels.append(x.category)
        values.append(x.amount)

    return render(request, 'chart.html', {
        'labels': labels,
        'values': values
    })
def edit_expense(request, id):
    item = get_object_or_404(Expense, id=id)

    if request.method == "POST":
        item.category = request.POST['category']
        item.amount = request.POST['amount']
        item.date = request.POST['date']
        item.save()
        return redirect('/history/')

    return render(request, 'edit.html', {'item': item})