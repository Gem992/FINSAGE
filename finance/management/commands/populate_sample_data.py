from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from finance.models import Income, Expense
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate sample data for the last 3 months'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Username to create data for')

    def handle(self, *args, **options):
        username = options['username']
        
        # Get or create user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': f'{username}@example.com'}
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(f'Created user: {username}')
        else:
            self.stdout.write(f'Using existing user: {username}')

        # Clear existing data for this user
        Income.objects.filter(user=user).delete()
        Expense.objects.filter(user=user).delete()
        self.stdout.write('Cleared existing data')

        # Sample data categories
        income_categories = [
            'Salary', 'Freelance', 'Investment', 'Bonus', 'Rental Income',
            'Side Business', 'Consulting', 'Online Sales', 'Commission'
        ]
        
        expense_categories = [
            'Food & Dining', 'Transportation', 'Housing', 'Utilities', 'Entertainment',
            'Healthcare', 'Shopping', 'Education', 'Travel', 'Insurance',
            'Groceries', 'Restaurants', 'Gas', 'Public Transport', 'Rent',
            'Electricity', 'Internet', 'Phone', 'Movies', 'Gym'
        ]

        # Generate data for last 6 months to ensure good chart data
        end_date = timezone.now()
        start_date = end_date - timedelta(days=180)
        
        current_date = start_date.replace(day=1)  # Start from beginning of month
        total_income = 0
        total_expense = 0

        while current_date <= end_date:
            # Generate 2-5 income entries per month
            num_incomes = random.randint(2, 5)
            for _ in range(num_incomes):
                category = random.choice(income_categories)
                amount = random.uniform(1000, 15000)
                # Create timezone-aware date
                random_day = random.randint(1, 28)  # Avoid month-end issues
                date = timezone.make_aware(
                    datetime.combine(
                        current_date.replace(day=random_day).date(),
                        datetime.min.time()
                    )
                )
                
                Income.objects.create(
                    user=user,
                    name=category,
                    amount=round(amount, 2),
                    date=date
                )
                total_income += amount

            # Generate 8-15 expense entries per month
            num_expenses = random.randint(8, 15)
            for _ in range(num_expenses):
                category = random.choice(expense_categories)
                amount = random.uniform(50, 2000)
                # Create timezone-aware date
                random_day = random.randint(1, 28)  # Avoid month-end issues
                date = timezone.make_aware(
                    datetime.combine(
                        current_date.replace(day=random_day).date(),
                        datetime.min.time()
                    )
                )
                
                Expense.objects.create(
                    user=user,
                    name=category,
                    amount=round(amount, 2),
                    date=date
                )
                total_expense += amount

            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- Total Income: ₹{total_income:.2f}\n'
                f'- Total Expenses: ₹{total_expense:.2f}\n'
                f'- Net Balance: ₹{total_income - total_expense:.2f}\n'
                f'- Data spans: {start_date.strftime("%Y-%m")} to {end_date.strftime("%Y-%m")}'
            )
        ) 