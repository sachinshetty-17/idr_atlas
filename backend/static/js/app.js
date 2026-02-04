async function searchGene() {
    const query = document.getElementById("searchBox").value;

    const response = await fetch(`/idrs?search=${query}`);
    const data = await response.json();

    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    if (data.length === 0) {
        resultsDiv.innerHTML = "<p>No results found</p>";
        return;
    }

    data.forEach(item => {
        const div = document.createElement("div");
        div.className = "card";
        div.innerHTML = `
            <strong>${item.gene}</strong><br>
            UniProt: ${item.accession}
        `;
        resultsDiv.appendChild(div);
    });
}

