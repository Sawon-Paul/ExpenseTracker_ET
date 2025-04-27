let transactionsData = [];

async function loadTransactions(filterType = "") {
    const tableBody = document.querySelector("#transactionTable tbody");
    tableBody.innerHTML = "<tr><td colspan='6'>Loading...</td></tr>";

    try {
        const url = filterType ? `/api/transactions?type=${filterType}` : '/api/transactions';
        const response = await fetch(url);
        const data = await response.json();
        transactionsData = data;
        if (Array.isArray(data) && data.length > 0) {
            tableBody.innerHTML = "";
            data.forEach(tx => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${tx.type}</td>
                    <td>${tx.subtype}</td>
                    <td>${tx.amount}</td>
                    <td>${tx.description}</td>
                    <td>${new Date(tx.timestamp).toLocaleString()}</td>
                    <td>${tx.tags || ''}</td>
                `;
                tableBody.appendChild(row);
            });
            renderChart(data);

        } else {
            tableBody.innerHTML = "<tr><td colspan='6'>No transactions found.</td></tr>";
        }
    } catch (error) {
        console.error("Error loading transactions:", error);
        tableBody.innerHTML = "<tr><td colspan='6'>Error loading data</td></tr>";
    }
}

const subtypes = {
    cash_in: ['salary', 'gift', 'refund'],
    cash_out: ['purchase', 'bill', 'donation']
};

function updateSubtypes() {
    const typeSelect = document.getElementById('type');
    const subtypeSelect = document.getElementById('subtype');
    const selectedType = typeSelect.value;

    subtypeSelect.innerHTML = '';
    subtypes[selectedType].forEach(subtype => {
        const option = document.createElement('option');
        option.value = subtype;
        option.textContent = subtype.charAt(0).toUpperCase() + subtype.slice(1);
        subtypeSelect.appendChild(option);
    });
}

async function handleQuickAdd(event) {
    event.preventDefault();

    const type = document.getElementById('type').value;
    const subtype = document.getElementById('subtype').value;
    const amount = document.getElementById('amount').value;
    const description = document.getElementById('description').value;
    const tags = document.getElementById('tags').value;

    const payload = { type, subtype, amount, description, tags };

    try {
        const response = await fetch('/api/transactions/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            event.target.reset();
            updateSubtypes(); // reset subtypes based on default type
            loadTransactions(); // reload table
        } else {
            alert('Failed to add transaction');
        }
    } catch (error) {
        console.error('Error submitting transaction:', error);
    }
}

function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const [key, val] = cookie.trim().split('=');
        if (key === name) return decodeURIComponent(val);
    }
    return '';
}


document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('toggleSidebar');
    const sidebar = document.getElementById('sidebar');

    toggleButton?.addEventListener('click', () => {
        sidebar.classList.toggle('hide');
    });

    document.querySelector('.donate-btn')?.addEventListener('click', () => {
        const formContainer = document.getElementById('donateFormContainer');
        formContainer.classList.toggle('hidden');
    });

    document.getElementById('logoutButton')?.addEventListener('click', () => {
        window.location.href = '/logout';
    });

    const filterDropdown = document.getElementById("transactionFilter");
    filterDropdown?.addEventListener("change", () => {
        loadTransactions(filterDropdown.value);
    });


    loadTransactions();

    const typeSelect = document.getElementById('type');
    typeSelect?.addEventListener('change', updateSubtypes);
    updateSubtypes(); 

    const quickAddForm = document.querySelector('.quick-add form');
    quickAddForm?.addEventListener('submit', handleQuickAdd);
});

function exportToCSV(){
    const headers = ["Type", "Subtype", "Amount", "Description", "Timestamp", "Tags"];
    const rows = [headers.join(",")];

    transactionsData.forEach(tx => {
        const row = [
            tx.type,
            tx.subtype,
            tx.amount,
            tx.description,
            new Date(tx.timestamp).toLocaleString(),
            tx.tags || ""
        ];
        rows.push(row.map(value => `"${value}"`).join(","));
    });

    const csvContent = rows.join("\n");
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "transactions.csv";
    a.click();

    URL.revokeObjectURL(url);
}
window.exportToCSV = exportToCSV;

function renderChart(data) {

    const canvas = document.getElementById("transactionChart");
    if (!canvas) {
        console.warn("Canvas element with id 'transactionChart' not found.");
        return;
    }
    const ctx = canvas.getContext("2d");


    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Aggregate totals for cash_in and cash_out
    const totals = { cash_in: 0, cash_out: 0 };
    data.forEach(tx => {
        if (tx.type === "cash_in" || tx.type === "cash_out") {
            totals[tx.type] += parseFloat(tx.amount);
        }
    });

    // Data for the chart
    const labels = ["Cash In", "Cash Out"];
    const values = [totals.cash_in, totals.cash_out];

    const maxVal = Math.max(...values);
    const barWidth = 100;
    const spacing = 50;
    const baseY = 250;

    // Draw the bars (for Cash In and Cash Out)
    values.forEach((val, i) => {
        const barHeight = (val / maxVal) * 200;
        ctx.fillStyle = i === 0 ? "#28a745" : "#dc3545"; // Green for cash_in, Red for cash_out
        ctx.fillRect(i * (barWidth + spacing) + spacing, baseY - barHeight, barWidth, barHeight);
        ctx.fillStyle = "#000";
        ctx.fillText(labels[i], i * (barWidth + spacing) + spacing + 10, baseY + 20); // Label under the bar
        ctx.fillText(val.toFixed(2), i * (barWidth + spacing) + spacing + 10, baseY - barHeight - 10); // Value on top of the bar
    });
}
