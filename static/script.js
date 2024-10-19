document.getElementById('register-button').addEventListener('click', function() {
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
});

document.getElementById('login-button').addEventListener('click', function() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.message === 'Logged in successfully!') {
            document.getElementById('auth-section').style.display = 'none';
            document.getElementById('transaction-section').style.display = 'block';
            document.getElementById('logout-button').style.display = 'inline-block';
            fetchTransactions();
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('logout-button').addEventListener('click', function() {
    fetch('/logout')
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            document.getElementById('auth-section').style.display = 'block';
            document.getElementById('transaction-section').style.display = 'none';
            document.getElementById('logout-button').style.display = 'none';
        });
});

document.getElementById('transaction-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const description = document.getElementById('transaction-description').value;
    const amount = parseFloat(document.getElementById('transaction-amount').value);
    const type = document.getElementById('transaction-type').value;

    fetch('/transactions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description, amount, type })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchTransactions();
    })
    .catch(error => console.error('Error:', error));
});

function fetchTransactions() {
    fetch('/transactions')
        .then(response => response.json())
        .then(data => {
            const transactionList = document.getElementById('transaction-list');
            transactionList.innerHTML = '';
            data.forEach(transaction => {
                const li = document.createElement('li');
                li.textContent = `${transaction.type}: $${transaction.amount} - ${transaction.description}`;
                transactionList.appendChild(li);
            });
        })
        .catch(error => console.error('Error:', error));
}
