document.addEventListener('DOMContentLoaded', function() {
    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Search form handling
    const searchForm = document.getElementById('search-form');
    const resultsContainer = document.getElementById('results-container');
    const loadingSpinner = document.createElement('div');
    loadingSpinner.className = 'loading-spinner mx-auto d-none';

    if (searchForm) {
        searchForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const query = document.getElementById('search-query').value;
            const source = document.getElementById('search-source').value;

            if (!query.trim()) {
                showAlert('Please enter a search query', 'error');
                return;
            }

            showLoading();
            try {
                const response = await fetch(`/search?query=${encodeURIComponent(query)}&source=${source}`);
                const data = await response.json();

                if (data.error) {
                    showAlert(data.error, 'error');
                    return;
                }

                displayResults(data.results);
            } catch (error) {
                showAlert('An error occurred while searching', 'error');
            } finally {
                hideLoading();
            }
        });
    }

    // Generate summary for a paper
    async function generateSummary(abstract, summaryContainer) {
        try {
            const response = await fetch('/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ abstract }),
            });

            const data = await response.json();
            if (data.error) {
                throw new Error(data.error);
            }

            summaryContainer.innerHTML = data.summary;
        } catch (error) {
            showAlert(error.message, 'error');
        }
    }

    function displayResults(results) {
        if (!results.length) {
            resultsContainer.innerHTML = '<p class="text-center text-secondary">No results found</p>';
            return;
        }

        resultsContainer.innerHTML = results.map(paper => `
            <div class="glass-card fade-in">
                <h3 class="mb-3">${paper.title}</h3>
                <p class="text-secondary mb-2">
                    ${paper.authors.join(', ')} | ${paper.published} | Source: ${paper.source}
                </p>
                <p class="mb-3">${paper.abstract}</p>
                <div class="d-flex gap-2">
                    <button class="btn btn-primary btn-sm" onclick="window.open('${paper.pdf_url}', '_blank')">
                        View PDF
                    </button>
                    <button class="btn btn-outline-primary btn-sm generate-summary" data-abstract="${encodeURIComponent(paper.abstract)}">
                        Generate Summary
                    </button>
                </div>
                <div class="summary-container mt-3 d-none"></div>
            </div>
        `).join('');

        // Add event listeners for summary generation
        document.querySelectorAll('.generate-summary').forEach(button => {
            button.addEventListener('click', function() {
                const abstract = decodeURIComponent(this.dataset.abstract);
                const summaryContainer = this.parentElement.nextElementSibling;
                summaryContainer.classList.remove('d-none');
                summaryContainer.innerHTML = '<div class="loading-spinner mx-auto"></div>';
                generateSummary(abstract, summaryContainer);
            });
        });
    }

    function showAlert(message, type) {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} fade-in`;
        alert.textContent = message;
        resultsContainer.prepend(alert);
        setTimeout(() => alert.remove(), 5000);
    }

    function showLoading() {
        loadingSpinner.classList.remove('d-none');
        resultsContainer.prepend(loadingSpinner);
    }

    function hideLoading() {
        loadingSpinner.classList.add('d-none');
    }
});
