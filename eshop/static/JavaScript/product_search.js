document.addEventListener("DOMContentLoaded", () => {

    const searchInput = document.getElementById("searchInput");
    const searchButton = document.getElementById("searchButton");
    const clearButton = document.getElementById("clearNormalSearch");
    const resultsContainer = document.getElementById("results");
    const liveResults = document.getElementById("liveResults");
    let debounce;

    // ==============================
    // LIVE SEARCH (suggestions dynamiques)
    // ==============================
    searchInput.addEventListener("input", () => {
        const query = searchInput.value.trim();
        liveResults.innerHTML = "";
        liveResults.style.display = "none";
        if (query.length < 1) return; // on commence dès le 1er caractère

        clearTimeout(debounce);
        debounce = setTimeout(async () => {
            try {
                const res = await fetch(`/product_search_result?q=${encodeURIComponent(query)}`);
                if (!res.ok) throw new Error("Server error");
                const data = await res.json();
                const products = Array.isArray(data) ? data : (data.results || []);
                if (!products.length) return;

                // afficher max 5 produits
                products.slice(0, 5).forEach(item => {
                    const li = document.createElement("li");
                    li.className = "list-group-item list-group-item-action d-flex justify-content-between align-items-center";
                    li.style.cursor = "pointer";
                    li.innerHTML = `
                        <span class="fw-bold">${item.name || "Produit sans nom"}</span>
                        <span class="badge bg-success rounded-pill">${item.price !== undefined ? item.price + " CHF" : "Prix indisponible"}</span>
                    `;
                    li.addEventListener("click", () => {
                        searchInput.value = item.name;
                        liveResults.innerHTML = "";
                        liveResults.style.display = "none";
                        fullSearch();
                    });
                    liveResults.appendChild(li);
                });

                liveResults.style.display = "block";

            } catch (err) {
                console.error(err);
            }
        }, 200); // debounce léger pour fluidité
    });

    // ==============================
    // FULL SEARCH (liste complète)
    // ==============================
    async function fullSearch() {
        const query = searchInput.value.trim();
        if (!query) return;

        liveResults.innerHTML = "";
        liveResults.style.display = "none";
        resultsContainer.innerHTML = "<p class='text-center mt-2'>Chargement...</p>";

        try {
            const res = await fetch(`/product_search_result/?q=${encodeURIComponent(query)}`);
            if (!res.ok) throw new Error("Server error");
            const data = await res.json();
            const products = Array.isArray(data) ? data : (data.results || []);

            resultsContainer.innerHTML = "";
            if (!products.length) {
                resultsContainer.innerHTML = "<p class='text-center mt-2'>Aucun produit trouvé</p>";
                return;
            }

            products.forEach(product => {
                const col = document.createElement("div");
                col.className = "col";
                col.innerHTML = `
                <div class="card h-100 shadow-sm border-0">
                    <img src="${product.image || '/static/images/no-image.png'}" class="card-img-top" style="height:250px; object-fit:cover;" alt="${product.name}">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title mb-3">
                            <a href="/product/${product.id}" class="text-decoration-none text-dark fw-bold">${product.name}</a>
                        </h5>
                        <div class="mt-auto">
                            ${product.availability ? `
                            <p class="fs-4 text-success fw-bold mb-2">${product.price} CHF</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="badge bg-success">En stock</span>
                                <div class="d-flex gap-2">
                                    <button class="btn btn-outline-primary btn-sm compare-btn" data-product-id="${product.id}">Comparer</button>
                                    <form action="/cart_add/${product.id}" method="post" class="m-0">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${getCSRF()}">
                                        <button type="submit" class="btn btn-primary btn-sm">
                                            <i class="fa fa-cart-plus"></i> Panier
                                        </button>
                                    </form>
                                </div>
                            </div>` :
                            `<p class="text-muted fst-italic mb-2">Victime de son succès...</p>
                             <span class="badge bg-danger">Rupture</span>`}
                        </div>
                    </div>
                </div>`;
                resultsContainer.appendChild(col);
            });

        } catch (err) {
            console.error(err);
            resultsContainer.innerHTML = "<p class='text-danger text-center mt-2'>Erreur lors du chargement des produits.</p>";
        }
    }

    // ==============================
    // ÉVÉNEMENTS
    // ==============================
    if (searchButton) searchButton.addEventListener("click", fullSearch);
    searchInput.addEventListener("keyup", (e) => { if (e.key === "Enter") fullSearch(); });

    if (clearButton) clearButton.addEventListener("click", () => {
        searchInput.value = "";
        resultsContainer.innerHTML = "";
        liveResults.innerHTML = "";
        liveResults.style.display = "none";
    });

    // ==============================
    // CSRF helper
    // ==============================
    function getCSRF() {
        const match = document.cookie.match(/csrftoken=([\w-]+)/);
        return match ? match[1] : "";
    }

    // ==============================
    // Clic en dehors pour fermer live search
    // ==============================
    document.addEventListener("click", (e) => {
        if (!searchInput.contains(e.target) && !liveResults.contains(e.target)) {
            liveResults.style.display = "none";
        }
    });

});