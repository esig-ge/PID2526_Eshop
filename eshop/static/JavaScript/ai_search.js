// ai_search.js

document.getElementById("ai_query_button").addEventListener("click", async function () {
    const query = document.getElementById("searchInput-ai").value;
    const resultsContainer = document.getElementById("ai_choice");

    // clean previous results
    resultsContainer.innerHTML = "";

    // if the request is too short, dont send do anything
    if (query.length < 2) {
        return;
    }

    try {
        const response = await fetch(`/ai_search?q=${encodeURIComponent(query)}`);

        if (!response.ok) {
            throw new Error(`Erreur HTTP ${response.status}`);
        }

        const data = await response.json();

        // if not in the expected format, show an error message
        if (!data.results || !Array.isArray(data.results) || data.results.length === 0) {
            resultsContainer.innerHTML = '<span style="color: #e74c3c;">Aucune suggestion pour le moment...</span>';
            return;
        }

        // take the element at index 0 (the one we need) and display it
        const suggestion = data.results[0];

        // ------------------------------------------------------
        // Treate the json to show cleanly the name and the price of the product, and make it a link to the product page
        // ------------------------------------------------------

        if (suggestion.name) {
            const card = document.createElement("div");
            card.style.padding = "16px";
            card.style.background = "#ffffff";
            card.style.borderRadius = "12px";
            card.style.boxShadow = "0 4px 12px rgba(0, 0, 0, 0.1)";
            card.style.marginTop = "12px";
            card.style.maxWidth = "400px";
            card.style.transition = "transform 0.2s ease";
            card.style.cursor = "pointer";  // Make the whole card clickable
            card.addEventListener("mouseover", () => { card.style.transform = "scale(1.02)"; });
            card.addEventListener("mouseout", () => { card.style.transform = "scale(1)"; });

            // Image (if available)
            if (suggestion.img_url) {
                const img = document.createElement("img");
                img.src = suggestion.img_url;
                img.alt = suggestion.name;
                img.style.width = "100%";
                img.style.height = "auto";
                img.style.borderRadius = "8px";
                img.style.marginBottom = "12px";
                card.appendChild(img);
            }

            // Title and Price as link
            const link = document.createElement("a");
            link.href = suggestion.link;
            link.style.textDecoration = "none";
            link.style.color = "#2c3e50";
            link.style.display = "block";
            link.innerHTML = `
            <h3 style="margin: 0; font-size: 1.2em; font-weight: 600;">${suggestion.name}</h3>
            <span style="color: #27ae60; font-size: 1.1em; font-weight: 500;">${suggestion.prix} CHF</span>
        `;
            card.appendChild(link);

            // Resume (description)
            if (suggestion.resume) {
                const p = document.createElement("p");
                p.style.marginTop = "8px";
                p.style.color = "#555";
                p.style.fontSize = "0.9em";
                p.style.lineHeight = "1.4";
                p.textContent = suggestion.resume;
                card.appendChild(p);
            }

            // Make the whole card clickable (redirect to link)
            card.addEventListener("click", () => { window.location.href = suggestion.link; });

            resultsContainer.appendChild(card);
        }

    } catch (err) {
        console.error("Erreur lors de la recherche IA :", err);
        resultsContainer.innerHTML = '<span style="color: #e74c3c;">Erreur de connexion à l\'IA...</span>';
    }
});

// Clear AI search
document.getElementById("clear-ai-search").addEventListener("click", function () {
    const input = document.getElementById("searchInput-ai");
    const results = document.getElementById("ai_choice");
    input.value = "";
    results.innerHTML = "";
});

// Clear normal search
document.getElementById("clear-normal-search").addEventListener("click", function () {
    const input = document.getElementById("searchInput");
    const results = document.getElementById("results");
    input.value = "";
    results.innerHTML = "";
});