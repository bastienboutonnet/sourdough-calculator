import streamlit as st
from pydantic import BaseModel, validator


class Starter(BaseModel):
    flour: float | int = 0
    water: float | int = 0
    combined: float | int = 0


class RecipieGrams(BaseModel):
    flour: float = 0.0
    water: float = 0.0
    starter: float = 0.0
    salt: float = 0.0

    @validator("*", allow_reuse=True)
    def round_grams(cls, v) -> int:
        return round(v, 1)  # type: ignore


def total_flour(
    target_weight: float, hydration_percent: float, starter_percent: float, salt_percent: float
) -> float:
    total_flour = target_weight * 100 / (100 + hydration_percent + salt_percent)
    return total_flour


def starter(total_flour: float, starter_percent: float, starter_hydration: float) -> Starter:
    combined = total_flour * starter_percent / 100.0
    flour = combined * 100 / (100 + starter_hydration)
    water = combined - flour
    return Starter(flour=flour, water=water, combined=combined)


def final_flour(total_flour: float, starter: Starter) -> float:
    final_flour = total_flour - starter.flour
    return final_flour


def water(total_flour: float, hydration_percent: float, starter: Starter) -> float:
    water = total_flour * hydration_percent / 100 - starter.water
    return water


def salt(total_flour: float, salt_percent: float) -> float:
    salt = total_flour * salt_percent / 100
    return salt


def calculate(
    target_weight, hydration_pct, salt_pct, starter_pct, starter_hydration
) -> RecipieGrams:
    _total_flour = total_flour(
        target_weight=target_weight,
        hydration_percent=hydration_pct,
        starter_percent=starter_pct,
        salt_percent=salt_pct,
    )
    _starter = starter(_total_flour, starter_pct, starter_hydration)
    _final_flour = final_flour(_total_flour, _starter)
    _water = water(_total_flour, hydration_pct, _starter)
    _salt = salt(_total_flour, salt_pct)

    recipe: RecipieGrams = RecipieGrams(
        flour=_final_flour, water=_water, starter=_starter.combined, salt=_salt
    )
    return recipe


def streamlit_app() -> int:
    st.title("Sourdough Calculator")

    target_weight: float = st.number_input("Target Loaf Weight (g)", value=1000, step=1)
    hydration: float = st.number_input("Dough Hydration %", value=70, max_value=100, min_value=1)
    starter: float = st.number_input("Starter %", value=20, min_value=1, max_value=100)
    salt: float = st.number_input("Salt %", value=2, min_value=1, max_value=100)
    starter_hydration: float = st.number_input(
        "Starter Hydration % (typically 100%)", value=100, min_value=1, max_value=100
    )
    recipe = calculate(
        target_weight=target_weight,
        hydration_pct=hydration,
        salt_pct=salt,
        starter_pct=starter,
        starter_hydration=starter_hydration,
    )
    st.markdown(
        f"**Flour**: {recipe.flour}g  |  "
        f"**Water**: {recipe.water}g  |  "
        f"**Starter**: {recipe.starter}g  |  "
        f"**Salt**: {recipe.salt}g"
    )
    return 0


if __name__ == "__main__":
    streamlit_app()
