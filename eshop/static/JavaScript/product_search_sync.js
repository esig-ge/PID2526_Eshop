
// Generé par IA, en se basant sur ma page product_search_sync.js crée antérieurement
document.getElementById("synced_input_button").addEventListener("click", function (event) {


    const query = document.getElementById("searchInput").value.trim();
    const resultsContainer = document.getElementById("results");

    resultsContainer.innerHTML = "";


    if (query.length < 1) {
        return;
    }

    try {
        const xhr = new XMLHttpRequest();
        xhr.open(
            "GET", `/ajax_search?q=${encodeURIComponent(query)}`, false);
        xhr.send(null);

        if (xhr.status !== 200) {
            throw new Error("Erreur serveur");
        }

        const data = JSON.parse(xhr.responseText);

        if (data.results.length === 0) {
            const li = document.createElement("li");
            li.textContent = "Aucun produit trouvé";
            li.style.color = "blue";
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
