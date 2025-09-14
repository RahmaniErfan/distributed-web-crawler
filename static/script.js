document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const searchResultsDiv = document.getElementById('search-results');
    const container = document.querySelector('.container');
    const header = document.querySelector('.header');
    const searchBox = document.querySelector('.search-box');
    const searchInputWrapper = document.querySelector('.search-input-wrapper');
    const paginationDiv = document.getElementById('pagination');
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');
    const pageInfoSpan = document.getElementById('page-info');

    let currentPage = 1;
    const resultsPerPage = 10; // Define how many results per page
    let totalPages = 1; // Will be updated by the backend

    // Function to update pagination UI
    const updatePaginationUI = () => {
        if (totalPages > 0) {
            pageInfoSpan.textContent = `Page ${currentPage} of ${totalPages}`;
            prevPageBtn.disabled = currentPage === 1;
            nextPageBtn.disabled = currentPage === totalPages;
            paginationDiv.style.display = 'flex'; // Show pagination if there are results
            pageInfoSpan.style.display = 'inline'; // Show page info
        } else {
            paginationDiv.style.display = 'none'; // Hide if no results
            pageInfoSpan.style.display = 'none'; // Hide page info
        }
    };

    const performSearch = async (page = 1) => {
        const query = searchInput.value.trim();
        currentPage = page; // Update current page

        if (!query) {
            searchResultsDiv.innerHTML = '<p class="no-results">Please enter a search query.</p>';
            // If no query, revert UI to initial state
            container.classList.remove('search-active');
            header.classList.remove('search-active');
            searchBox.classList.remove('search-active');
            searchInputWrapper.classList.remove('search-active');
            paginationDiv.style.display = 'none'; // Hide pagination
            return;
        }

        // Add active classes to change UI
        container.classList.add('search-active');
        header.classList.add('search-active');
        searchBox.classList.add('search-active');
        searchInputWrapper.classList.add('search-active');

        // Force reflow to ensure transitions are applied from the initial state
        void container.offsetHeight;

        // Start fading out current results
        searchResultsDiv.classList.add('fade-out');

        // Show "Searching..." message while fading out previous results
        setTimeout(() => {
            searchResultsDiv.innerHTML = '<p class="no-results">Searching...</p>';
        }, 150); // Half of the fade-out transition duration

        // After fade-out completes, fetch new results and fade them in
        setTimeout(async () => {
            try {
                const response = await fetch(`/search?query=${encodeURIComponent(query)}&page=${currentPage}&per_page=${resultsPerPage}`);
                const data = await response.json();

                searchResultsDiv.innerHTML = ''; // Clear "Searching..." message

                if (data.results.length === 0) {
                    searchResultsDiv.innerHTML = '<p class="no-results">No results found for your query.</p>';
                    totalPages = 0;
                    currentPage = 0;
                    updatePaginationUI();
                } else {
                    // Ensure pagination is visible when results are found
                    paginationDiv.style.display = 'flex';
                    pageInfoSpan.style.display = 'inline';
                    data.results.forEach(result => {
                        const resultDiv = document.createElement('div');
                        resultDiv.classList.add('search-result');
                        const title = result.title || 'No Title';
                        const url = result.url || '#';
                        const description = result.description || (result.body ? result.body.substring(0, 200) + '...' : 'No description available.');
                        resultDiv.innerHTML = `
                            <h2><a href="${url}" target="_blank" rel="noopener noreferrer">${title}</a></h2>
                            <p class="url">${url}</p>
                            <p>${description}</p>
                        `;
                        searchResultsDiv.appendChild(resultDiv);
                    });

                    totalPages = data.total_pages;
                    currentPage = data.current_page;
                    updatePaginationUI();
                }
            } catch (error) {
                console.error('Error during search:', error);
                searchResultsDiv.innerHTML = '<p class="no-results">An error occurred while performing the search. Please try again later.</p>';
                totalPages = 1;
                updatePaginationUI();
            } finally {
                searchResultsDiv.classList.remove('fade-out'); // Fade in new content
            }
        }, 300); // Wait for fade-out to complete before showing new content
    };

    searchInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            performSearch(); // Start search from page 1
        }
    });

    // Event listeners for pagination buttons
    prevPageBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            performSearch(currentPage - 1);
        }
    });

    nextPageBtn.addEventListener('click', () => {
        if (currentPage < totalPages) {
            performSearch(currentPage + 1);
        }
    });

    // Optional: Revert UI if search input is cleared after results are shown
    searchInput.addEventListener('input', () => {
        if (searchInput.value.trim() === '' && container.classList.contains('search-active')) {
            searchResultsDiv.innerHTML = ''; // Clear results
            container.classList.remove('search-active');
            header.classList.remove('search-active');
            searchBox.classList.remove('search-active');
            searchInputWrapper.classList.remove('search-active');
            paginationDiv.style.display = 'none'; // Hide pagination
            pageInfoSpan.style.display = 'none'; // Hide page info
            currentPage = 1; // Reset current page
            totalPages = 1; // Reset total pages
            updatePaginationUI(); // Update UI to reflect reset
        }
    });
});
