// ai_search.js

document.getElementById("aiQueryButton").addEventListener("click", async function () {
    const query = document.getElementById("searchInput-ai").value;
    const resultsContainer = document.getElementById("ai_choice");

    // clean previous results
    resultsContainer.innerHTML = "";

        // show loading spinner
    const loader = document.createElement("div");
    loader.style.textAlign = "center";
    loader.style.padding = "12px";
    loader.innerHTML = `
        <div style="
            width:24px;
            height:24px;
            border:3px solid #ddd;
            border-top:3px solid #3498db;
            border-radius:50%;
            animation: spin 0.8s linear infinite;
            margin:auto;
        "></div>
    `;
    resultsContainer.appendChild(loader);

    // inject animation once
    if (!document.getElementById("aiLoaderStyle")) {
        const style = document.createElement("style");
        style.id = "aiLoaderStyle";
        style.innerHTML = `
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
    }


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
        // remove loader
        loader.remove();

        // if not in the expected format, show an error message
        if (!data.results || !Array.isArray(data.results) || data.results.length === 0 || data.results[0].name === "Erreur de parsing") {
            resultsContainer.innerHTML = '<span style="color: #e74c3c;">Aucune suggestion pour le moment...</span> <p> Essayez de reformuler votre question ou d\'utiliser des mots-clés différents.</p>';
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
            // doesn't work ? 
            link.target = "_blank";
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