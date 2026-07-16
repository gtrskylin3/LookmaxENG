let currentWordsCount = 0;

async function updateWords() {
    try {
        const response = await fetch("/api/words/");

        if (!response.ok) {
            console.error("API error:", response.status);
            return;
        }

        const words = await response.json();

        const wordsList = document.getElementById("words-list");

        wordsList.innerHTML = "";
        console.log(words)
        for (const word of words) {
            const li = document.createElement("li");

            li.innerHTML = `
                <div class="word-info">
                    <span class="word-main">
                        ${word.word}
                    </span>

                    <span class="word-translate">
                        ${word.translate ?? ""}
                    </span>

                    ${
                        word.context
                            ? `
                                <span class="word-context">
                                    Context: ${word.context}
                                </span>
                            `
                            : ""
                    }
                </div>

                <div>
                    <form
                        action="/delete"
                        method="post"
                        style="display: inline;"
                    >
                        <input
                            type="hidden"
                            name="id"
                            value="${word.id}"
                        >

                        <button
                            type="submit"
                            class="btn-delete"
                            title="Delete"
                        >
                            ❌
                        </button>
                    </form>
                </div>
            `;

            wordsList.appendChild(li);
        }

    } catch (error) {
        console.error("Failed to load words:", error);
    }
}

updateWords();

setInterval(updateWords, 5000);