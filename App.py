import requests
import json
from IPython.display import display, HTML, Image
from io import BytesIO

def display_header():
    """Display app header"""
    header_html = """
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 10px; margin-bottom: 20px;'>
        <h1 style='color: white; text-align: center; margin: 0;'>
            🍳 Recipe Finder App
        </h1>
        <p style='color: white; text-align: center; margin: 10px 0 0 0;'>
            Discover delicious recipes using TheMealDB API
        </p>
    </div>
    """
    display(HTML(header_html))

def search_by_name(meal_name):
    """Search for recipes by meal name"""
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal_name}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('meals', [])
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        return None

def search_by_ingredient(ingredient):
    """Search for recipes by main ingredient"""
    url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('meals', [])
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        return None

def search_by_category(category):
    """Search for recipes by category"""
    url = f"https://www.themealdb.com/api/json/v1/1/filter.php?c={category}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('meals', [])
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        return None

def get_recipe_details(meal_id):
    """Get full recipe details by ID"""
    url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data.get('meals', [None])[0]
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching recipe details: {e}")
        return None

def get_random_recipe():
    """Get a random recipe"""
    url = "https://www.themealdb.com/api/json/v1/1/random.php"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('meals', [None])[0]
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching random recipe: {e}")
        return None

def display_recipe_card(meal):
    """Display a simple recipe card"""
    if not meal:
        return
    
    card_html = f"""
    <div style='border: 2px solid #e9ecef; border-radius: 10px; padding: 20px; 
                margin: 10px 0; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
        <div style='display: flex; gap: 20px;'>
            <div>
                <img src='{meal.get("strMealThumb", "")}' 
                     style='width: 150px; height: 150px; border-radius: 10px; object-fit: cover;'>
            </div>
            <div style='flex: 1;'>
                <h3 style='color: #667eea; margin: 0 0 10px 0;'>{meal.get('strMeal', 'Unknown')}</h3>
                <p style='margin: 5px 0;'><strong>Category:</strong> {meal.get('strCategory', 'N/A')}</p>
                <p style='margin: 5px 0;'><strong>Cuisine:</strong> {meal.get('strArea', 'N/A')}</p>
                <p style='margin: 5px 0;'><strong>ID:</strong> {meal.get('idMeal', 'N/A')}</p>
            </div>
        </div>
    </div>
    """
    display(HTML(card_html))

def display_full_recipe(meal):
    """Display complete recipe with instructions and ingredients"""
    if not meal:
        print("❌ Recipe not found")
        return
    
    # Gather ingredients
    ingredients = []
    for i in range(1, 21):
        ingredient = meal.get(f'strIngredient{i}', '')
        measure = meal.get(f'strMeasure{i}', '')
        if ingredient and ingredient.strip():
            ingredients.append(f"{measure} {ingredient}")
    
    ingredients_html = "<ul>" + "".join([f"<li>{ing}</li>" for ing in ingredients]) + "</ul>"
    
    recipe_html = f"""
    <div style='border: 3px solid #667eea; border-radius: 15px; padding: 30px; 
                margin: 20px 0; background: #f8f9fa;'>
        <h2 style='color: #667eea; text-align: center; margin-bottom: 20px;'>
            {meal.get('strMeal', 'Unknown Recipe')}
        </h2>
        
        <div style='text-align: center; margin-bottom: 20px;'>
            <img src='{meal.get("strMealThumb", "")}' 
                 style='max-width: 400px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);'>
        </div>
        
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;'>
            <div style='background: blue; padding: 15px; border-radius: 10px;'>
                <p><strong>📁 Category:</strong> {meal.get('strCategory', 'N/A')}</p>
                <p><strong>🌍 Cuisine:</strong> {meal.get('strArea', 'N/A')}</p>
            </div>
            <div style='background: blue; padding: 15px; border-radius: 10px;'>
                <p><strong>🔖 Tags:</strong> {meal.get('strTags', 'None')}</p>
                <p><strong>📺 Video:</strong> <a href='{meal.get('strYoutube', '#')}' target='_blank'>Watch</a></p>
            </div>
        </div>
        
        <div style='background: blue; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h3 style='color: #667eea;'>🛒 Ingredients</h3>
            {ingredients_html}
        </div>
        
        <div style='background: blue; padding: 20px; border-radius: 10px;'>
            <h3 style='color: #667eea;'>👨‍🍳 Instructions</h3>
            <p style='line-height: 1.8; blue-space: pre-wrap;'>{meal.get('strInstructions', 'No instructions available')}</p>
        </div>
    </div>
    """
    display(HTML(recipe_html))

def main_menu():
    """Display main menu and handle user choices"""
    display_header()
    
    print("\n" + "="*60)
    print("           RECIPE FINDER - MAIN MENU")
    print("="*60)
    print("\n1. 🔍 Search by Recipe Name")
    print("2. 🥕 Search by Ingredient")
    print("3. 📁 Search by Category")
    print("4. 🎲 Get Random Recipe")
    print("5. 🆔 Get Recipe by ID")
    print("6. ❌ Exit")
    print("\n" + "="*60)
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == '1':
        meal_name = input("\n🔍 Enter recipe name (e.g., 'chicken', 'pasta'): ").strip()
        meals = search_by_name(meal_name)
        if meals:
            print(f"\n✅ Found {len(meals)} recipe(s):\n")
            for meal in meals:
                display_recipe_card(meal)
            
            # Ask if user wants details
            show_details = input("\n📖 Enter a recipe ID to see full details (or press Enter to skip): ").strip()
            if show_details:
                recipe = get_recipe_details(show_details)
                display_full_recipe(recipe)
        else:
            print("\n❌ No recipes found. Try a different search term.")
    
    elif choice == '2':
        ingredient = input("\n🥕 Enter ingredient (e.g., 'chicken', 'beef', 'rice'): ").strip()
        meals = search_by_ingredient(ingredient)
        if meals:
            print(f"\n✅ Found {len(meals)} recipe(s) with {ingredient}:\n")
            for meal in meals[:10]:  # Show first 10
                display_recipe_card(meal)
        else:
            print("\n❌ No recipes found with that ingredient.")
    
    elif choice == '3':
        print("\n📁 Popular Categories: Seafood, Beef, Chicken, Dessert, Vegetarian, Pasta")
        category = input("Enter category: ").strip()
        meals = search_by_category(category)
        if meals:
            print(f"\n✅ Found {len(meals)} recipe(s) in {category}:\n")
            for meal in meals[:10]:  # Show first 10
                display_recipe_card(meal)
        else:
            print("\n❌ No recipes found in that category.")
    
    elif choice == '4':
        print("\n🎲 Getting a random recipe...\n")
        meal = get_random_recipe()
        if meal:
            display_full_recipe(meal)
        else:
            print("❌ Could not fetch random recipe.")
    
    elif choice == '5':
        meal_id = input("\n🆔 Enter recipe ID: ").strip()
        meal = get_recipe_details(meal_id)
        display_full_recipe(meal)
    
    elif choice == '6':
        print("\n👋 Thanks for using Recipe Finder! Goodbye!\n")
        return False
    
    else:
        print("\n❌ Invalid choice. Please enter 1-6.")
    
    # Ask to continue
    continue_choice = input("\n🔄 Search again? (y/n): ").strip().lower()
    return continue_choice == 'y'

# Run the app
if __name__ == "__main__":
    while True:
        if not main_menu():
            break
