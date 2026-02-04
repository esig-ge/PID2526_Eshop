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
            const li = document.createElement("li");
            li.textContent = "Aucun produit trouvé";
            li.style.color = "red";
            resultsContainer.appendChild(li);
            return;
        }

        data.results.forEach(item => {
            const li = document.createElement("li");
            const a = document.createElement("a");

            a.href = `/get/${item.id}/`;

            // Correction principale : on protège contre les valeurs undefined
            const name = item.name || "Produit sans nom";
            const price = item.price !== undefined ? item.price : "";

            // On n’affiche le tiret et le prix que si le prix existe
            a.textContent = price 
                ? `${name} — ${price} €`
                : name;

            li.appendChild(a);
            resultsContainer.appendChild(li);
        });

    } catch (err) {
        console.error(err);
        const li = document.createElement("li");
        li.textContent = "Erreur de recherche";
        li.style.color = "red";
        resultsContainer.appendChild(li);
    }
});