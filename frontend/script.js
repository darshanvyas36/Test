document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = 'http://localhost:8000';

    // --- DOM Elements ---
    const addAccountForm = document.getElementById('add-account-form');
    const accountList = document.getElementById('account-list');
    const createContentForm = document.getElementById('create-content-form');
    const loadingOverlay = document.getElementById('loading-overlay');
    const loadingMessage = document.getElementById('loading-message');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const promptInput = document.getElementById('prompt');
    const hashtagsInput = document.getElementById('hashtags');

    // --- State ---
    let accounts = [];

    // --- UI & Loading Functions ---

    const showLoading = (message) => {
        loadingMessage.textContent = message;
        loadingOverlay.classList.remove('hidden');
    };

    const hideLoading = () => {
        loadingOverlay.classList.add('hidden');
    };

    const renderAccounts = () => {
        accountList.innerHTML = '';
        if (accounts.length === 0) {
            accountList.innerHTML = '<li>No accounts added yet.</li>';
            return;
        }
        accounts.forEach(account => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span>${account.username}</span>
                <div class="button-group">
                    <button class="post-btn" data-id="${account.id}">Post</button>
                    <button class="delete-btn" data-id="${account.id}">Delete</button>
                </div>
            `;
            accountList.appendChild(li);
        });
    };

    // --- API Functions ---

    const fetchAndRenderAccounts = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/accounts`);
            if (!response.ok) throw new Error('Failed to fetch accounts.');
            accounts = await response.json();
            renderAccounts();
        } catch (error) {
            console.error('Error fetching accounts:', error);
            alert('Could not fetch accounts. Make sure the backend is running.');
        }
    };

    const handleAddAccount = async (event) => {
        event.preventDefault();
        showLoading('Adding account...');
        try {
            const response = await fetch(`${API_BASE_URL}/accounts`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: usernameInput.value, password: passwordInput.value }),
            });
            if (!response.ok) throw new Error((await response.json()).detail);
            addAccountForm.reset();
            await fetchAndRenderAccounts();
        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            hideLoading();
        }
    };

    const handleDeleteAccount = async (accountId) => {
        if (!confirm('Are you sure you want to delete this account?')) return;
        showLoading('Deleting account...');
        try {
            const response = await fetch(`${API_BASE_URL}/accounts/${accountId}`, { method: 'DELETE' });
            if (!response.ok) throw new Error('Failed to delete account.');
            await fetchAndRenderAccounts();
        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            hideLoading();
        }
    };

    const handlePostToSingleAccount = async (accountId) => {
        const prompt = promptInput.value;
        const hashtags = hashtagsInput.value;
        if (!prompt || !hashtags) {
            alert('Please fill in the prompt and hashtags fields first.');
            return;
        }
        showLoading(`Starting content pipeline for one account... This may take several minutes.`);
        try {
            const response = await fetch(`${API_BASE_URL}/orchestration/run-for-account`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ account_id: accountId, simple_prompt: prompt, hashtags }),
            });
            if (!response.ok) throw new Error((await response.json()).detail);
            const result = await response.json();
            alert(`Pipeline finished for account! Status: ${result.status}.`);
        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            hideLoading();
        }
    };

    const handlePostToAll = async (event) => {
        event.preventDefault();
        if (accounts.length === 0) {
            alert('Please add at least one account first.');
            return;
        }
        showLoading('Starting content pipeline for ALL accounts... This may take several minutes.');
        try {
            const response = await fetch(`${API_BASE_URL}/orchestration/run-for-all`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ simple_prompt: promptInput.value, hashtags: hashtagsInput.value }),
            });
            if (!response.ok) throw new Error((await response.json()).detail);
            const results = await response.json();
            const successCount = results.filter(r => r.status === 'success').length;
            alert(`Pipeline finished!\n\nSuccessful posts: ${successCount}\nFailed posts: ${results.length - successCount}`);
        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            hideLoading();
        }
    };

    // --- Event Listeners ---
    addAccountForm.addEventListener('submit', handleAddAccount);
    createContentForm.addEventListener('submit', handlePostToAll);

    accountList.addEventListener('click', (event) => {
        const target = event.target;
        const accountId = target.dataset.id;
        if (target.classList.contains('delete-btn')) {
            handleDeleteAccount(accountId);
        } else if (target.classList.contains('post-btn')) {
            handlePostToSingleAccount(accountId);
        }
    });

    // --- Initial Load ---
    fetchAndRenderAccounts();
});
