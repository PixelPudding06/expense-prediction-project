from django.http import HttpResponse
from reportlab.pdfgen import canvas
import os
from dotenv import load_dotenv
from google import genai
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from sklearn.linear_model import LinearRegression
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('/login/')

    return render(request, 'register.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/login/')
def welcome(request):
    return render(request, 'welcome.html')
def mimi_chat(request):
    user_message = request.GET.get("msg")

    prompt = f"""
    You are Mimi, a cute smart finance assistant for Expense Prediction Pro.
    Reply in short, friendly and useful style.
    User: {user_message}
    """

    response = model.generate_content(prompt)

    return JsonResponse({
        "reply": response.text
    })
def mimi_chat(request):
    try:
        user_message = request.GET.get("msg", "")

        prompt = f"""
You are Mimi, a cute smart finance assistant for Expense Prediction Pro.
Reply short, friendly and useful.
User: {user_message}
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return JsonResponse({
            "reply": response.text
        })

    except Exception as e:
        return JsonResponse({
            "reply": str(e)
        })
def download_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Expense_Report.pdf"'

    p = canvas.Canvas(response)

    # Title
    p.setFont("Helvetica-Bold", 22)
    p.drawString(170, 800, "Expense Report")

    # Subtitle
    p.setFont("Helvetica", 12)
    p.drawString(180, 780, "Expense Prediction Pro")

    # Line
    p.line(40, 770, 550, 770)

    # Heading
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 740, "Category")
    p.drawString(230, 740, "Amount")
    p.drawString(380, 740, "Date")

    y = 710
    total = 0

    expenses = Expense.objects.all()

    p.setFont("Helvetica", 12)

    for x in expenses:
        p.drawString(50, y, str(x.category))
        p.drawString(230, y, "Rs " + str(x.amount))
        p.drawString(380, y, str(x.date))

        total += x.amount
        y -= 25

        if y < 80:
            p.showPage()
            y = 800

    # Total
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y-20, "Total Expense: Rs " + str(total))

    # Footer
    p.setFont("Helvetica", 10)
    p.drawString(180, 40, "Generated by Expense Prediction Pro")

    p.save()
    return response