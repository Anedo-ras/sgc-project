// Main JavaScript functionality

// Handle recipe form submission
document.addEventListener('DOMContentLoaded', function() {
    const recipeForm = document.getElementById('recipe-form');
    if (recipeForm) {
        recipeForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const ingredientsSelect = document.getElementById('ingredients');
            const selectedIngredients = Array.from(ingredientsSelect.selectedOptions)
                .map(option => option.value);
            
            if (selectedIngredients.length === 0) return;
            
            try {
                const response = await fetch('/api/recipe/suggest', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ ingredients: selectedIngredients })
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    // Display recipes
                    const container = document.getElementById('recipes-container');
                    container.innerHTML = '';
                    
                    result.recipes.forEach(recipe => {
                        const recipeCard = document.createElement('div');
                        recipeCard.className = 'recipe-card';
                        
                        let ingredientsList = '';
                        if (Array.isArray(recipe.ingredients)) {
                            ingredientsList = recipe.ingredients.map(ing => 
                                `<li>${ing}</li>`
                            ).join('');
                        } else {
                            ingredientsList = `<li>${recipe.ingredients}</li>`;
                        }
                        
                        recipeCard.innerHTML = `
                            <div class="recipe-content">
                                <h3>${recipe.name}</h3>
                                <h4>Ingredients:</h4>
                                <ul>${ingredientsList}</ul>
                                <h4>Instructions:</h4>
                                <p>${recipe.instructions}</p>
                            </div>
                        `;
                        
                        container.appendChild(recipeCard);
                    });
                    
                    document.getElementById('recipes-result').style.display = 'block';
                    
                    // Clear the form
                    ingredientsSelect.selectedIndex = -1;
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                console.error('Error getting recipes:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }
    
    // IntaSend payment integration
    const upgradeButtons = document.querySelectorAll('#upgrade-btn');
    upgradeButtons.forEach(button => {
        button.addEventListener('click', function() {
            // This would integrate with IntaSend API in a real implementation
            alert('IntaSend payment integration would be implemented here. In a real app, this would redirect to a payment page.');
        });
    });
});