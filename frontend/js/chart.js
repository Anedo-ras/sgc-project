// Mood chart functionality
let moodChart = null;

function renderMoodChart(moodData) {
    const ctx = document.getElementById('mood-chart').getContext('2d');
    
    if (moodChart) {
        moodChart.destroy();
    }
    
    // Process data for chart
    const labels = moodData.map(entry => new Date(entry.created_at).toLocaleDateString());
    const scores = moodData.map(entry => entry.score);
    const sentiments = moodData.map(entry => entry.sentiment);
    
    const backgroundColors = sentiments.map(sentiment => {
        switch(sentiment) {
            case 'POSITIVE': return 'rgba(46, 204, 113, 0.7)';
            case 'NEGATIVE': return 'rgba(231, 76, 60, 0.7)';
            default: return 'rgba(241, 196, 15, 0.7)';
        }
    });
    
    moodChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Mood Score',
                data: scores,
                backgroundColor: backgroundColors,
                borderColor: 'rgba(52, 152, 219, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1
                }
            }
        }
    });
}

// Load mood history from API
async function loadMoodHistory() {
    try {
        const response = await fetch('/api/mood/entries');
        const data = await response.json();
        
        if (data && data.length > 0) {
            renderMoodChart(data);
            document.getElementById('mood-result').style.display = 'block';
        }
    } catch (error) {
        console.error('Error loading mood history:', error);
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadMoodHistory();
    
    // Handle mood form submission
    const moodForm = document.getElementById('mood-form');
    if (moodForm) {
        moodForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const journalText = document.getElementById('journal-entry').value;
            if (!journalText) return;
            
            try {
                const response = await fetch('/api/mood/entry', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text: journalText })
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    // Update UI with result
                    document.getElementById('sentiment-label').textContent = result.sentiment.label;
                    document.getElementById('sentiment-score').textContent = 
                        (result.sentiment.score * 100).toFixed(1) + '%';
                    
                    // Reload the chart with updated data
                    loadMoodHistory();
                    
                    // Clear the form
                    document.getElementById('journal-entry').value = '';
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                console.error('Error submitting journal entry:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }
});