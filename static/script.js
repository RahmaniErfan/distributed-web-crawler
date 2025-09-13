document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button'); // This button is removed, but keeping the variable for now
    const searchResultsDiv = document.getElementById('search-results');

    const performSearch = async () => {
        const query = searchInput.value.trim();
        if (!query) {
            searchResultsDiv.innerHTML = '<p class="no-results">Please enter a search query.</p>';
            return;
        }

        searchResultsDiv.innerHTML = '<p class="no-results">Searching...</p>';

        try {
            const response = await fetch(`/search?query=${encodeURIComponent(query)}`);
            const results = await response.json();

            searchResultsDiv.innerHTML = ''; // Clear previous results

            if (results.length === 0) {
                searchResultsDiv.innerHTML = '<p class="no-results">No results found for your query.</p>';
                return;
            }

            results.forEach(result => {
                const resultDiv = document.createElement('div');
                resultDiv.classList.add('search-result');

                const title = result.title || 'No Title';
                const url = result.url || '#';
                const description = result.description || result.body ? result.body.substring(0, 200) + '...' : 'No description available.';

                resultDiv.innerHTML = `
                    <h2><a href="${url}" target="_blank" rel="noopener noreferrer">${title}</a></h2>
                    <p class="url">${url}</p>
                    <p>${description}</p>
                `;
                searchResultsDiv.appendChild(resultDiv);
            });

        } catch (error) {
            console.error('Error during search:', error);
            searchResultsDiv.innerHTML = '<p class="no-results">An error occurred while performing the search. Please try again later.</p>';
        }
    };

    // searchButton.addEventListener('click', performSearch); // Removed as per user request

    searchInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            performSearch();
        }
    });
});
