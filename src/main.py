import streamlit as st

from formulae import calculate


def streamlit_app() -> int:
    st.title("Sourdough Calculator")

    target_weight: float = st.number_input("Target Loaf Weight (g)", value=1200, step=1)
    hydration: float = st.number_input("Dough Hydration %", value=70, max_value=100, min_value=1)
    starter: float = st.number_input("Starter %", value=20, min_value=1, max_value=100)
    salt: float = st.number_input("Salt %", value=2, min_value=1, max_value=100)
    starter_hydration: float = st.number_input(
        "Starter Hydration % (typically 100%)", value=100, min_value=1, max_value=100
    )
    taste_flour: float = st.number_input("Secondary (for taste) Flour %", value=20, max_value=100)
    recipe = calculate(
        target_weight=target_weight,
        hydration_pct=hydration,
        salt_pct=salt,
        starter_pct=starter,
        starter_hydration=starter_hydration,
        taste_flour_pct=taste_flour,
    )
    secondary_flour_conditional = ""
    if recipe.taste_flour:
        secondary_flour_conditional = f"- **Second Flour** {recipe.taste_flour}g\n"
    st.header("Ingredients:")
    st.markdown(
        f"- **Flour**: {recipe.flour}g \n"
        f"{secondary_flour_conditional}"
        f"- **Water**: {recipe.water}g\n"
        f"- **Starter**: {recipe.starter}g\n"
        f"- **Salt**: {recipe.salt}g"
    )
    return 0


if __name__ == "__main__":
    streamlit_app()
