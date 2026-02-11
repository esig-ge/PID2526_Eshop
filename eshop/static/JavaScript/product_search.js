document.getElementById("searchInput").addEventListener("input", async function () {

    const query = this.value.trim();
    const resultsContainer = document.getElementById("results");

    resultsContainer.innerHTML = "";

    if (query.length < 1) {
        return;   // on sort directement, pas besoin de créer un <li> vide
    }

    try {
        const response = await fetch(`/ajax_search?q=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error("Erreur serveur");

        const data = await response.json();

        if (data.results.length === 0) {
            const div = document.createElement("div");
            div.className = "alert alert-warning mt-2";
            div.textContent = "Aucun produit trouvé";
            resultsContainer.appendChild(div);
            return;
        }

        // Use Bootstrap list-group for pretty display
        const listGroup = document.createElement("div");
        listGroup.className = "list-group mt-2";

        data.results.forEach(item => {
            const a = document.createElement("a");
            a.href = `/get/${item.id}/`;
            a.className = "list-group-item list-group-item-action d-flex justify-content-between align-items-center";
            a.style.textDecoration = "none";

            // Protection contre undefined
            const name = item.name || "Produit sans nom";
            const price = item.price !== undefined ? item.price : "Prix indisponible";

            a.innerHTML = `
                <span class="fw-bold">${name}</span>
                <span class="badge bg-success rounded-pill">${price} €</span>
            `;

            listGroup.appendChild(a);
        });

        resultsContainer.appendChild(listGroup);

    } catch (err) {
        console.error(err);
        const div = document.createElement("div");
        div.className = "alert alert-danger mt-2";
        div.textContent = "Erreur de recherche";
        resultsContainer.appendChild(div);
    }
});