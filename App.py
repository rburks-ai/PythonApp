import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Recipe Finder",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'search'
if 'selected_recipe' not in st.session_state:
    st.session_state.selected_recipe = None

# API Functions
@st.cache_data(ttl=3600)
def search_by_name(meal_name):
    """Search for recipes by meal name"""
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('meals', [])
    except:
        return None

@st.cache_data(ttl=3600)
def search_by_ingredient(ingredient):
    """Search for recipes by main ingredient"""
    url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('meals', [])
    except:
        return None

@st.cache_data(ttl=3600)
def search_by_category(category):
    """Search for recipes by category"""
    url = f"https://www.themealdb.com/api/json/v1/1/filter.php?c={category}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('meals', [])
    except:
        return None

@st.cache_data(ttl=3600)
def get_recipe_details(meal_id):
    """Get full recipe details by ID"""
    url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('meals', [None])[0]
    except:
        return None

@st.cache_data(ttl=3600)
def get_random_recipe():
    """Get a random recipe"""
    url = "https://www.themealdb.com/api/json/v1/1/random.php"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('meals', [None])[0]
    except:
        return None

@st.cache_data(ttl=3600)
def get_all_categories():
    """Get all available categories"""
    url = "https://www.themealdb.com/api/json/v1/1/categories.php"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [cat['strCategory'] for cat in data.get('categories', [])]
    except:
        return ["Seafood", "Beef", "Chicken", "Dessert", "Vegetarian", "Pasta", "Lamb"]

def display_recipe_card(meal, show_details_button=True):
    """Display a recipe card"""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            response = requests.get(meal.get("strMealThumb", ""))
            img = Image.open(BytesIO(response.content))
            st.image(img, use_container_width=True)
        except:
            st.image("https://via.placeholder.com/300x300?text=No+Image", use_container_width=True)
    
    with col2:
        st.subheader(meal.get('strMeal', 'Unknown'))
        st.write(f"**Category:** {meal.get('strCategory', 'N/A')}")
        st.write(f"**Cuisine:** {meal.get('strArea', 'N/A')}")
        
        if show_details_button:
            if st.button(f"View Full Recipe 👉", key=f"btn_{meal.get('idMeal')}"):
                st.session_state.selected_recipe = meal.get('idMeal')
                st.session_state.current_view = 'details'
                st.rerun()

def display_full_recipe(meal):
    """Display complete recipe with all details"""
    if not meal:
        st.error("Recipe not found")
        return
    
    # Back button
    if st.button("← Back to Search"):
        st.session_state.current_view = 'search'
        st.session_state.selected_recipe = None
        st.rerun()
    
    st.title(meal.get('strMeal', 'Unknown Recipe'))
    
    # Image
    col1, col2 = st.columns([1, 1])
    with col1:
        try:
            response = requests.get(meal.get("strMealThumb", ""))
            img = Image.open(BytesIO(response.content))
            st.image(img, use_container_width=True)
        except:
            st.image("https://via.placeholder.com/400x400?text=No+Image", use_container_width=True)
    
    with col2:
        st.subheader("Recipe Info")
        st.write(f"**📁 Category:** {meal.get('strCategory', 'N/A')}")
        st.write(f"**🌍 Cuisine:** {meal.get('strArea', 'N/A')}")
        st.write(f"**🔖 Tags:** {meal.get('strTags', 'None')}")
        
        if meal.get('strYoutube'):
            st.markdown(f"**📺 [Watch Video Tutorial]({meal.get('strYoutube')})**")
        
        if meal.get('strSource'):
            st.markdown(f"**🔗 [Original Source]({meal.get('strSource')})**")
    
    st.divider()
    
    # Ingredients
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🛒 Ingredients")
        ingredients = []
        for i in range(1, 21):
            ingredient = meal.get(f'strIngredient{i}', '')
            measure = meal.get(f'strMeasure{i}', '')
            if ingredient and ingredient.strip():
                ingredients.append(f"{measure} {ingredient}")
        
        for ing in ingredients:
            st.write(f"• {ing}")
    
    with col2:
        st.subheader("👨‍🍳 Instructions")
        instructions = meal.get('strInstructions', 'No instructions available')
        st.write(instructions)

# Main App
def main():
    # Header
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0;'>🍳 Recipe Finder</h1>
        <p style='color: white; margin: 0.5rem 0 0 0;'>Discover delicious recipes from around the world!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show recipe details if selected
    if st.session_state.current_view == 'details' and st.session_state.selected_recipe:
        recipe = get_recipe_details(st.session_state.selected_recipe)
        display_full_recipe(recipe)
        return
    
    # Sidebar
    with st.sidebar:
        st.header("🔍 Search Options")
        
        search_type = st.radio(
            "Search by:",
            ["Recipe Name", "Ingredient", "Category", "Random Recipe"],
            help="Choose how you want to search for recipes"
        )
        
        st.divider()
        
        results = None
        
        if search_type == "Recipe Name":
            st.subheader("Search by Name")
            meal_name = st.text_input("Enter recipe name:", placeholder="e.g., chicken curry, pasta")
            if st.button("🔍 Search", key="search_name"):
                if meal_name:
                    with st.spinner("Searching..."):
                        results = search_by_name(meal_name)
                        st.session_state.search_results = results
                else:
                    st.warning("Please enter a recipe name")
        
        elif search_type == "Ingredient":
            st.subheader("Search by Ingredient")
            ingredient = st.text_input("Enter ingredient:", placeholder="e.g., chicken, beef, rice")
            if st.button("🔍 Search", key="search_ingredient"):
                if ingredient:
                    with st.spinner("Searching..."):
                        results = search_by_ingredient(ingredient)
                        st.session_state.search_results = results
                else:
                    st.warning("Please enter an ingredient")
        
        elif search_type == "Category":
            st.subheader("Search by Category")
            categories = get_all_categories()
            category = st.selectbox("Select category:", categories)
            if st.button("🔍 Search", key="search_category"):
                with st.spinner("Searching..."):
                    results = search_by_category(category)
                    st.session_state.search_results = results
        
        elif search_type == "Random Recipe":
            st.subheader("Get Random Recipe")
            st.info("Click below to get a surprise recipe!")
            if st.button("🎲 Get Random Recipe", key="random"):
                with st.spinner("Finding a recipe..."):
                    random_recipe = get_random_recipe()
                    if random_recipe:
                        st.session_state.selected_recipe = random_recipe.get('idMeal')
                        st.session_state.current_view = 'details'
                        st.rerun()
        
        st.divider()
        st.caption("Powered by TheMealDB API")
    
    # Main content area
    if 'search_results' in st.session_state and st.session_state.search_results:
        results = st.session_state.search_results
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Recipes", len(results))
        with col2:
            categories = set(r.get('strCategory', 'N/A') for r in results if r.get('strCategory'))
            st.metric("Categories", len(categories))
        with col3:
            cuisines = set(r.get('strArea', 'N/A') for r in results if r.get('strArea'))
            st.metric("Cuisines", len(cuisines))
        
        st.divider()
        
        # Display results
        st.subheader(f"Found {len(results)} Recipe(s)")
        
        for meal in results:
            with st.container():
                display_recipe_card(meal)
                st.divider()
    
    elif 'search_results' in st.session_state and st.session_state.search_results is not None:
        st.info("No recipes found. Try a different search term!")
    
    else:
        # Welcome message
        st.markdown("""
        ### Welcome to Recipe Finder! 👋
        
        Use the sidebar to start searching for delicious recipes:
        
        - 🔍 **Search by Name** - Find specific recipes like "chicken curry" or "chocolate cake"
        - 🥕 **Search by Ingredient** - Discover recipes using ingredients you have
        - 📁 **Search by Category** - Browse recipes by type (Seafood, Dessert, etc.)
        - 🎲 **Random Recipe** - Get surprise recipe suggestions
        
        Start exploring and happy cooking! 🍳
        """)
        
        # Show some example images
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("https://www.themealdb.com/images/media/meals/llcbn01574260722.jpg", caption="Delicious Recipes")
        with col2:
            st.image("https://www.themealdb.com/images/media/meals/wvpsxx1468256321.jpg", caption="From Around the World")
        with col3:
            st.image("https://www.themealdb.com/images/media/meals/ytpstt1511814614.jpg", caption="Easy to Make")

if __name__ == "__main__":
    main()
