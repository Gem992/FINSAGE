function signupUser() {
  const username = document.getElementById('signup-username').value;
  const email = document.getElementById('signup-email').value;
  const password = document.getElementById('signup-password').value;

  localStorage.setItem("finsageUser", JSON.stringify({ username, email, password }));
  alert("Sign up successful!");
  window.location.href = "login.html";
  return false;
}

function loginUser() {
  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;
  const savedUser = JSON.parse(localStorage.getItem("finsageUser"));

  if (savedUser && savedUser.email === email && savedUser.password === password) {
    localStorage.setItem("finsageLoggedIn", "true");
    alert("Login successful!");
    window.location.href = "dashboard.html";
  } else {
    alert("Invalid credentials!");
  }
  return false;
}

function logout() {
  localStorage.setItem("finsageLoggedIn", "false");
  alert("Logged out!");
  window.location.href = "index.html";
}

// Income and expense entry
function addIncome() {
  const name = document.getElementById('income-name').value;
  const amount = parseFloat(document.getElementById('income-amount').value);
  if (!name || isNaN(amount)) {
    alert("Enter valid income!");
    return false;
  }

  const incomes = JSON.parse(localStorage.getItem("finsageIncomes")) || [];
  incomes.push({ name, amount, date: new Date().toISOString() });
  localStorage.setItem("finsageIncomes", JSON.stringify(incomes));

  document.getElementById('income-name').value = "";
  document.getElementById('income-amount').value = "";

  loadDashboard();
  return false;
}

function addExpense() {
  const name = document.getElementById('expense-name').value;
  const amount = parseFloat(document.getElementById('expense-amount').value);
  if (!name || isNaN(amount)) {
    alert("Enter valid expense!");
    return false;
  }

  const expenses = JSON.parse(localStorage.getItem("finsageExpenses")) || [];
  expenses.push({ name, amount, date: new Date().toISOString() });
  localStorage.setItem("finsageExpenses", JSON.stringify(expenses));

  document.getElementById('expense-name').value = "";
  document.getElementById('expense-amount').value = "";

  loadDashboard();
  return false;
}

function loadDashboard() {
  const user = JSON.parse(localStorage.getItem("finsageUser"));
  document.getElementById("username").textContent = user.username;

  const incomes = JSON.parse(localStorage.getItem("finsageIncomes")) || [];
  const expenses = JSON.parse(localStorage.getItem("finsageExpenses")) || [];

  const totalIncome = incomes.reduce((sum, i) => sum + i.amount, 0);
  const totalExpenses = expenses.reduce((sum, e) => sum + e.amount, 0);
  const netBalance = totalIncome - totalExpenses;

  document.getElementById("total-income").textContent = totalIncome.toFixed(2);
  document.getElementById("total-expenses").textContent = totalExpenses.toFixed(2);
  document.getElementById("net-balance").textContent = netBalance.toFixed(2);

  generateMonthlyReport(incomes, expenses);
}

function generateMonthlyReport(incomes, expenses) {
  const list = document.getElementById("monthly-report-list");
  list.innerHTML = "";

  const now = new Date();
  const thisMonth = now.getMonth();
  const thisYear = now.getFullYear();

  const filteredIncomes = incomes.filter(item => new Date(item.date).getMonth() === thisMonth && new Date(item.date).getFullYear() === thisYear);
  const filteredExpenses = expenses.filter(item => new Date(item.date).getMonth() === thisMonth && new Date(item.date).getFullYear() === thisYear);

  list.innerHTML += `<li><strong>Incomes:</strong></li>`;
  filteredIncomes.forEach(i => {
    list.innerHTML += `<li>+ ₹${i.amount} - ${i.name}</li>`;
  });

  list.innerHTML += `<li><strong>Expenses:</strong></li>`;
  filteredExpenses.forEach(e => {
    list.innerHTML += `<li>- ₹${e.amount} - ${e.name}</li>`;
  });
}

window.onload = function () {
  if (window.location.pathname.includes("dashboard.html")) {
    const loggedIn = localStorage.getItem("finsageLoggedIn");
    const user = JSON.parse(localStorage.getItem("finsageUser"));
    if (loggedIn !== "true" || !user) {
      alert("Please log in first.");
      window.location.href = "login.html";
      return;
    }
    loadDashboard();
  }
};