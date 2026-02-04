// ai_search.js

document.getElementById("ai_query_button").addEventListener("click", async function () {
    const query = document.getElementById("searchInput-ai").value;
    const resultsContainer = document.getElementById("ai_choice");

    // On vide le conteneur à chaque nouvelle saisie
    resultsContainer.innerHTML = "";

    // Si la requête est trop courte → on ne fait rien
    if (query.length < 2) {
        return;
    }

    try {
        const response = await fetch(`/ai_search?q=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error(`Erreur HTTP ${response.status}`);
        }

        const data = await response.json();

        // Cas où il n'y a pas de résultat ou format inattendu
        if (!data.results || !Array.isArray(data.results) || data.results.length === 0) {
            resultsContainer.innerHTML = '<span style="color: #e74c3c;">Aucune suggestion pour le moment...</span>';
            return;
        }

        // On prend le premier élément (souvent le plus pertinent)
        const suggestion = data.results[0];

        // ------------------------------------------------------
        // Cas 1 : c'est juste du texte brut (recommandation IA)
        // ------------------------------------------------------
        if (typeof suggestion === 'string') {
            const div = document.createElement("div");
            div.style.padding = "8px 12px";
            div.style.background = "#f8f9fa";
            div.style.borderRadius = "6px";
            div.style.marginTop = "8px";
            div.innerHTML = `<strong>Suggestion IA :</strong> ${suggestion}`;
            resultsContainer.appendChild(div);
            return;
        }

        // ------------------------------------------------------
        // Cas 2 : c'est un objet {id, name, price} → on fait un lien
        // ------------------------------------------------------
        if (suggestion.name) {
            const link = document.createElement("a");
            link.href = `/get/${suggestion.id}/`;   // ← adapte selon ton URL
            link.style.textDecoration = "none";
            link.style.color = "#2c3e50";
            link.style.fontWeight = "500";
            link.innerHTML = `
                <strong>${suggestion.name}</strong>
                <span style="color:#27ae60; margin-left:10px;">${suggestion.price} CHF</span>
            `;

            const div = document.createElement("div");
            div.style.padding = "8px 12px";
            div.style.background = "#e8f4f8";
            div.style.borderRadius = "6px";
            div.style.marginTop = "8px";
            div.appendChild(link);

            resultsContainer.appendChild(div);
        }

    } catch (err) {
        console.error("Erreur lors de la recherche IA :", err);
        resultsContainer.innerHTML = '<span style="color: #e74c3c;">Erreur de connexion à l\'IA...</span>';
    }
});