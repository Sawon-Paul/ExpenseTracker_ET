// ✅ Global function: can now be used in HTML onclick
async function loadTransactions(filterType = "") {
    const tableBody = document.querySelector("#transactionTable tbody");
    tableBody.innerHTML = "<tr><td colspan='5'>Loading...</td></tr>";

    try {
        const url = filterType ? `/api/transactions?type=${filterType}` : '/api/transactions';
        const response = await fetch(url);
        const data = await response.json();

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
                `;
                tableBody.appendChild(row);
            });
        } else {
            tableBody.innerHTML = "<tr><td colspan='5'>No transactions found.</td></tr>";
        }
    } catch (error) {
        console.error("Error loading transactions:", error);
        tableBody.innerHTML = "<tr><td colspan='5'>Error loading data</td></tr>";
    }
}

// ✅ Runs when DOM is ready
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

    const logoutButton = document.getElementById('logoutButton');
    logoutButton?.addEventListener('click', () => {
        window.location.href = '/logout';
    });

    const filterDropdown = document.getElementById("transactionFilter");
    filterDropdown?.addEventListener("change", () => {
        loadTransactions(filterDropdown.value);
    });

    // 🔄 Load all transactions initially
    loadTransactions();
});
