// Flashcard functionality
function createFlashcardElement(question, answer) {
    const flashcard = document.createElement('div');
    flashcard.className = 'flashcard';
    
    const inner = document.createElement('div');
    inner.className = 'flashcard-inner';
    
    const front = document.createElement('div');
    front.className = 'flashcard-front';
    front.innerHTML = `<h4>${question}</h4><p>Click to flip</p>`;
    
    const back = document.createElement('div');
    back.className = 'flashcard-back';
    back.innerHTML = `<p>${answer}</p>`;
    
    inner.appendChild(front);
    inner.appendChild(back);
    flashcard.appendChild(inner);
    
    flashcard.addEventListener('click', function() {
        this.classList.toggle('flipped');
    });
    
    return flashcard;
}

// Handle study form submission
document.addEventListener('DOMContentLoaded', function() {
    const studyForm = document.getElementById('study-form');
    if (studyForm) {
        studyForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const studyNotes = document.getElementById('study-notes').value;
            if (!studyNotes) return;
            
            try {
                const response = await fetch('/api/study/flashcards', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ notes: studyNotes })
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    // Display flashcards
                    const container = document.getElementById('flashcards-container');
                    container.innerHTML = '';
                    
                    result.flashcards.forEach(card => {
                        const flashcardElement = createFlashcardElement(
                            card.question, 
                            card.answer
                        );
                        container.appendChild(flashcardElement);
                    });
                    
                    document.getElementById('flashcards-result').style.display = 'block';
                    
                    // Clear the form
                    document.getElementById('study-notes').value = '';
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                console.error('Error generating flashcards:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }
});