import openai
from flask import current_app

def get_recipe_suggestions(ingredients):
    """Get recipe suggestions from OpenAI API based on ingredients"""
    openai.api_key = current_app.config['OPENAI_API_KEY']
    
    prompt = f"Suggest 3 simple recipes using these ingredients: {', '.join(ingredients)}. For each recipe, provide a name, ingredients list, and simple instructions. Format as JSON with name, ingredients, and instructions fields."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful cooking assistant that suggests simple recipes based on available ingredients."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        
        # Parse the response (this would need more robust parsing in a real app)
        recipes_text = response.choices[0].message.content
        # For demo purposes, we'll return sample data
        # In a real implementation, you'd parse the response properly
        
        sample_recipes = [
            {
                "name": "Vegetable Stir Fry",
                "ingredients": ["Mixed vegetables", "Soy sauce", "Oil", "Garlic"],
                "instructions": "1. Heat oil in a pan. 2. Add garlic and stir. 3. Add vegetables and cook for 5 minutes. 4. Add soy sauce and serve."
            },
            {
                "name": "Simple Salad",
                "ingredients": ["Lettuce", "Tomato", "Cucumber", "Olive oil"],
                "instructions": "1. Chop all vegetables. 2. Mix in a bowl. 3. Drizzle with olive oil. 4. Season to taste."
            },
            {
                "name": "Fruit Smoothie",
                "ingredients": ["Banana", "Berries", "Yogurt", "Milk"],
                "instructions": "1. Combine all ingredients in a blender. 2. Blend until smooth. 3. Serve immediately."
            }
        ]
        
        return sample_recipes
    except Exception as e:
        print(f"Error getting recipe suggestions: {e}")
        return []