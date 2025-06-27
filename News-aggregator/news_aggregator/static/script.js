async function fetchNews() {
    const query = document.getElementById("search-query").value || "India";
    const newsResponse = await fetch(`/news?query=${query}`);
    const newsArticles = await newsResponse.json();
    
    const imageResponse = await fetch(`https://pixabay.com/api/?key=49225244-4c2c651867908e3eb46a522c5&q=${query}&image_type=photo`);
    const imageData = await imageResponse.json();
    const images = imageData.hits || [];
    
    const container = document.getElementById("news-container");
    container.innerHTML = "";  // Clear old results
    
    newsArticles.forEach((article, index) => {
        const card = document.createElement("div");
        card.className = "news-card fade-in";

        // Choose the best available image (either from the article or Pixabay)
        let imageUrl = article.urlToImage || (images[index] ? images[index].webformatURL : "default.jpg");

        card.innerHTML = `
            <img src="${imageUrl}" alt="News Image" class="news-image"/>
            <h3>${article.title}</h3>
            <p><strong>Source:</strong> ${article.source.name || "Unknown"}</p>
            <a href="${article.url}" target="_blank">Read more</a>
        `;
        container.appendChild(card);
    });
}

// CSS Animation Class
const style = document.createElement("style");
style.innerHTML = `
    .fade-in { animation: fadeIn 0.8s ease-in-out; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .news-image { width: 100%; border-radius: 10px; margin-bottom: 10px; }
`;
document.head.appendChild(style);

// Load news on page load
fetchNews();
