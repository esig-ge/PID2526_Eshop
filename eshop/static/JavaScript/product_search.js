
// Generé par IA, modifier extensivement pour repondre a mes besoins
document.getElementById("searchInput").addEventListener("input",  async function () {

    const query = this.value.trim();
    const resultsContainer = document.getElementById("results");


    // Vider proprement tous les enfants
    while (resultsContainer.firstChild) {
        resultsContainer.removeChild(resultsContainer.firstChild);
    }

    if (query.length < 1) {
        const li = document.createElement("li");
        resultsContainer.clear
        return;
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
            a.textContent = `${item.name} — ${item.price} €`;


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
