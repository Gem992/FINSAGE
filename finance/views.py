from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime, timedelta
import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import base64
from collections import defaultdict
import numpy as np
import seaborn as sns

from .models import Income, Expense

def health_check(request):
    """Comprehensive health check endpoint for Railway"""
    try:
        # Test database connectivity
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Test if we can query the models
        User.objects.count()  # Just check if we can access the database
        
        return JsonResponse({
            'status': 'healthy',
            'service': 'finsage',
            'database': 'connected',
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'service': 'finsage',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=500)

def index(request):
    return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('dashboard')
    
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def dashboard(request):
    user = request.user
    selected_month = request.GET.get('month', timezone.now().strftime('%Y-%m'))
    
    # Parse selected month
    try:
        selected_date = datetime.strptime(selected_month, '%Y-%m')
        selected_date = timezone.make_aware(selected_date)
        start_date = selected_date.replace(day=1)
        if selected_date.month == 12:
            end_date = selected_date.replace(year=selected_date.year + 1, month=1, day=1)
        else:
            end_date = selected_date.replace(month=selected_date.month + 1, day=1)
    except:
        selected_date = timezone.now()
        start_date = selected_date.replace(day=1)
        end_date = (selected_date.replace(day=1) + timedelta(days=32)).replace(day=1)
    
    incomes = Income.objects.filter(user=user, date__gte=start_date, date__lt=end_date)
    expenses = Expense.objects.filter(user=user, date__gte=start_date, date__lt=end_date)
    
    total_income = sum(income.amount for income in incomes)
    total_expenses = sum(expense.amount for expense in expenses)
    net_balance = total_income - total_expenses
    
    # Get available months for dropdown
    all_incomes = Income.objects.filter(user=user)
    all_expenses = Expense.objects.filter(user=user)
    
    available_months = set()
    for income in all_incomes:
        available_months.add(income.date.strftime('%Y-%m'))
    for expense in all_expenses:
        available_months.add(expense.date.strftime('%Y-%m'))
    
    # Add current month if no data exists
    current_month = timezone.now().strftime('%Y-%m')
    available_months.add(current_month)
    available_months = sorted(list(available_months), reverse=True)
    
    context = {
        'user': user,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': net_balance,
        'monthly_incomes': incomes,
        'monthly_expenses': expenses,
        'selected_month': selected_month,
        'available_months': available_months,
    }
    
    return render(request, 'dashboard.html', context)

@csrf_exempt
@login_required
def add_income(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        amount = data.get('amount')
        date_str = data.get('date', timezone.now().strftime('%Y-%m-%d'))
        
        if name and amount:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
                date = timezone.make_aware(date)
                Income.objects.create(
                    user=request.user,
                    name=name,
                    amount=amount,
                    date=date
                )
                return JsonResponse({'success': True})
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid date format'})
    
    return JsonResponse({'success': False})

@csrf_exempt
@login_required
def add_expense(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        amount = data.get('amount')
        date_str = data.get('date', timezone.now().strftime('%Y-%m-%d'))
        
        if name and amount:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
                date = timezone.make_aware(date)
                Expense.objects.create(
                    user=request.user,
                    name=name,
                    amount=amount,
                    date=date
                )
                return JsonResponse({'success': True})
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid date format'})
    
    return JsonResponse({'success': False})

@csrf_exempt
@login_required
def update_income(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        income_id = data.get('id')
        name = data.get('name')
        amount = data.get('amount')
        date_str = data.get('date')
        
        try:
            income = Income.objects.get(id=income_id, user=request.user)
            if name:
                income.name = name
            if amount:
                income.amount = amount
            if date_str:
                date = datetime.strptime(date_str, '%Y-%m-%d')
                income.date = timezone.make_aware(date)
            income.save()
            return JsonResponse({'success': True})
        except Income.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Income not found'})
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid date format'})
    
    return JsonResponse({'success': False})

@csrf_exempt
@login_required
def update_expense(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        expense_id = data.get('id')
        name = data.get('name')
        amount = data.get('amount')
        date_str = data.get('date')
        
        try:
            expense = Expense.objects.get(id=expense_id, user=request.user)
            if name:
                expense.name = name
            if amount:
                expense.amount = amount
            if date_str:
                date = datetime.strptime(date_str, '%Y-%m-%d')
                expense.date = timezone.make_aware(date)
            expense.save()
            return JsonResponse({'success': True})
        except Expense.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Expense not found'})
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid date format'})
    
    return JsonResponse({'success': False})

@csrf_exempt
@login_required
def delete_income(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        income_id = data.get('id')
        
        try:
            income = Income.objects.get(id=income_id, user=request.user)
            income.delete()
            return JsonResponse({'success': True})
        except Income.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Income not found'})
    
    return JsonResponse({'success': False})

@csrf_exempt
@login_required
def delete_expense(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        expense_id = data.get('id')
        
        try:
            expense = Expense.objects.get(id=expense_id, user=request.user)
            expense.delete()
            return JsonResponse({'success': True})
        except Expense.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Expense not found'})
    
    return JsonResponse({'success': False})

@login_required
def generate_charts(request):
    user = request.user
    selected_month = request.GET.get('month', timezone.now().strftime('%Y-%m'))
    
    # Parse selected month
    try:
        selected_date = datetime.strptime(selected_month, '%Y-%m')
        selected_date = timezone.make_aware(selected_date)
        start_date = selected_date.replace(day=1)
        if selected_date.month == 12:
            end_date = selected_date.replace(year=selected_date.year + 1, month=1, day=1)
        else:
            end_date = selected_date.replace(month=selected_date.month + 1, day=1)
    except:
        selected_date = timezone.now()
        start_date = selected_date.replace(day=1)
        end_date = (selected_date.replace(day=1) + timedelta(days=32)).replace(day=1)
    
    incomes = Income.objects.filter(user=user, date__gte=start_date, date__lt=end_date)
    expenses = Expense.objects.filter(user=user, date__gte=start_date, date__lt=end_date)
    
    # Income distribution chart
    income_data = defaultdict(float)
    for income in incomes:
        income_data[income.name] += float(income.amount)
    
    if income_data:
        plt.figure(figsize=(8, 6))
        plt.pie(income_data.values(), labels=income_data.keys(), autopct='%1.1f%%')
        plt.title(f'Income Distribution - {selected_month}')
        
        # Save to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        income_chart = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
    else:
        income_chart = None
    
    # Expense distribution chart
    expense_data = defaultdict(float)
    for expense in expenses:
        expense_data[expense.name] += float(expense.amount)
    
    if expense_data:
        plt.figure(figsize=(8, 6))
        plt.pie(expense_data.values(), labels=expense_data.keys(), autopct='%1.1f%%')
        plt.title(f'Expense Distribution - {selected_month}')
        
        # Save to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        expense_chart = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
    else:
        expense_chart = None
    
    # Line graph for monthly trends (last 6 months)
    line_chart = generate_line_chart(user)
    
    # Bar graph for category comparison (all time)
    bar_chart = generate_bar_chart(user)
    
    # Histogram for amount distribution (selected month)
    histogram_chart = generate_histogram(user, start_date, end_date)
    
    # Heatmap for monthly patterns (last 6 months)
    heatmap_chart = generate_heatmap(user)
    
    context = {
        'income_chart': income_chart,
        'expense_chart': expense_chart,
        'line_chart': line_chart,
        'bar_chart': bar_chart,
        'histogram_chart': histogram_chart,
        'heatmap_chart': heatmap_chart,
        'selected_month': selected_month,
    }
    
    return render(request, 'charts.html', context)

def generate_line_chart(user):
    """Generate line chart showing monthly trends"""
    # Get last 6 months of data
    end_date = timezone.now()
    start_date = end_date - timedelta(days=180)
    
    incomes = Income.objects.filter(user=user, date__gte=start_date)
    expenses = Expense.objects.filter(user=user, date__gte=start_date)
    
    # Group by month
    income_by_month = defaultdict(float)
    expense_by_month = defaultdict(float)
    
    for income in incomes:
        month_key = income.date.strftime('%Y-%m')
        income_by_month[month_key] += float(income.amount)
    
    for expense in expenses:
        month_key = expense.date.strftime('%Y-%m')
        expense_by_month[month_key] += float(expense.amount)
    
    months = sorted(list(set(list(income_by_month.keys()) + list(expense_by_month.keys()))))
    
    if months:
        plt.figure(figsize=(12, 6))
        income_values = [income_by_month.get(month, 0) for month in months]
        expense_values = [expense_by_month.get(month, 0) for month in months]
        
        plt.plot(months, income_values, marker='o', linewidth=2, label='Income', color='green')
        plt.plot(months, expense_values, marker='s', linewidth=2, label='Expenses', color='red')
        
        plt.title('Monthly Income vs Expenses Trend (Last 6 Months)')
        plt.xlabel('Month')
        plt.ylabel('Amount (₹)')
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        line_chart = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        return line_chart
    return None

def generate_bar_chart(user):
    """Generate bar chart comparing income and expense categories"""
    incomes = Income.objects.filter(user=user)
    expenses = Expense.objects.filter(user=user)
    
    income_categories = defaultdict(float)
    expense_categories = defaultdict(float)
    
    for income in incomes:
        income_categories[income.name] += float(income.amount)
    
    for expense in expenses:
        expense_categories[expense.name] += float(expense.amount)
    
    if income_categories or expense_categories:
        plt.figure(figsize=(14, 8))
        
        # Prepare data
        categories = list(set(list(income_categories.keys()) + list(expense_categories.keys())))
        income_values = [income_categories.get(cat, 0) for cat in categories]
        expense_values = [expense_categories.get(cat, 0) for cat in categories]
        
        x = np.arange(len(categories))
        width = 0.35
        
        plt.bar(x - width/2, income_values, width, label='Income', color='green', alpha=0.7)
        plt.bar(x + width/2, expense_values, width, label='Expenses', color='red', alpha=0.7)
        
        plt.title('Income vs Expenses by Category (All Time)')
        plt.xlabel('Categories')
        plt.ylabel('Amount (₹)')
        plt.legend()
        plt.xticks(x, categories, rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        bar_chart = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        return bar_chart
    return None

def generate_histogram(user, start_date=None, end_date=None):
    """Generate histogram showing amount distribution for selected month"""
    if start_date and end_date:
        incomes = Income.objects.filter(user=user, date__gte=start_date, date__lt=end_date)
        expenses = Expense.objects.filter(user=user, date__gte=start_date, date__lt=end_date)
        title_suffix = f" - {start_date.strftime('%Y-%m')}"
    else:
        incomes = Income.objects.filter(user=user)
        expenses = Expense.objects.filter(user=user)
        title_suffix = " (All Time)"
    
    income_amounts = [float(income.amount) for income in incomes]
    expense_amounts = [float(expense.amount) for expense in expenses]
    
    if income_amounts or expense_amounts:
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        if income_amounts:
            plt.hist(income_amounts, bins=20, alpha=0.7, color='green', edgecolor='black')
            plt.title(f'Income Amount Distribution{title_suffix}')
            plt.xlabel('Amount (₹)')
            plt.ylabel('Frequency')
            plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 2, 2)
        if expense_amounts:
            plt.hist(expense_amounts, bins=20, alpha=0.7, color='red', edgecolor='black')
            plt.title(f'Expense Amount Distribution{title_suffix}')
            plt.xlabel('Amount (₹)')
            plt.ylabel('Frequency')
            plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        histogram_chart = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        return histogram_chart
    return None

def generate_heatmap(user):
    """Generate heatmap showing monthly patterns"""
    # Get last 6 months
    end_date = timezone.now()
    start_date = end_date - timedelta(days=180)
    
    incomes = Income.objects.filter(user=user, date__gte=start_date)
    expenses = Expense.objects.filter(user=user, date__gte=start_date)
    
    # Create monthly data matrix
    months = []
    current_date = start_date.replace(day=1)
    while current_date <= end_date:
        months.append(current_date.strftime('%Y-%m'))
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
    
    # Get unique categories
    income_categories = set(income.name for income in incomes)
    expense_categories = set(expense.name for expense in expenses)
    all_categories = list(income_categories) + list(expense_categories)
    
    if months and all_categories:
        # Create data matrix
        data_matrix = np.zeros((len(all_categories), len(months)))
        
        for i, category in enumerate(all_categories):
            for j, month in enumerate(months):
                month_start = datetime.strptime(month, '%Y-%m')
                month_start = timezone.make_aware(month_start)
                if month_start.month == 12:
                    month_end = month_start.replace(year=month_start.year + 1, month=1)
                else:
                    month_end = month_start.replace(month=month_start.month + 1)
                
                # Sum amounts for this category and month
                category_incomes = incomes.filter(name=category, date__gte=month_start, date__lt=month_end)
                category_expenses = expenses.filter(name=category, date__gte=month_start, date__lt=month_end)
                
                total = sum(float(inc.amount) for inc in category_incomes) + sum(float(exp.amount) for exp in category_expenses)
                data_matrix[i, j] = total
        
        plt.figure(figsize=(14, 8))
        sns.heatmap(data_matrix, 
                   xticklabels=months, 
                   yticklabels=all_categories,
                   cmap='YlOrRd', 
                   annot=True, 
                   fmt='.0f',
                   cbar_kws={'label': 'Amount (₹)'})
        
        plt.title('Monthly Category Heatmap (Last 6 Months)')
        plt.xlabel('Month')
        plt.ylabel('Category')
        plt.xticks(rotation=45)
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        heatmap_chart = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        return heatmap_chart
    return None
