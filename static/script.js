// static/script.js

// Sign-Up Handler
document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            const response = await fetch('/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            });
            const result = await response.json();
            document.getElementById('signupMessage').innerText = result.message || result.error;
        });
    }

    // Login Handler
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;

            const response = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const result = await response.json();
            document.getElementById('loginMessage').innerText = result.message;

            if (response.ok) window.location.href = '/dashboard';
        });
    }

    // Logout Handler
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', async () => {
            await fetch('/logout');
            window.location.href = '/login';
        });
    }

    // Add Favorite Handler
    const favoriteForm = document.getElementById('favoriteForm');
    if (favoriteForm) {
        favoriteForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const title = document.getElementById('title').value;
            const mediaType = document.getElementById('mediaType').value;

            const response = await fetch('/add_favorite', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, media_type: mediaType })
            });
            const result = await response.json();
            alert(result.message);
            loadFavorites();
        });
    }

    // Load Favorites on Dashboard
    async function loadFavorites() {
        const favoritesList = document.getElementById('favoritesList');
        favoritesList.innerHTML = '';

        const response = await fetch('/favorites');
        const favorites = await response.json();

        favorites.forEach(favorite => {
            const li = document.createElement('li');
            li.textContent = `${favorite.title} (${favorite.media_type})`;
            favoritesList.appendChild(li);
        });
    }

    if (document.getElementById('favoritesList')) {
        loadFavorites();
    }
});
