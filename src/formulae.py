from pydantic import BaseModel, validator


class Starter(BaseModel):
    flour: float = 0
    water: float = 0
    combined: float = 0


class RecipieGrams(BaseModel):
    flour: float = 0.0
    water: float = 0.0
    starter: float = 0.0
    salt: float = 0.0
    taste_flour: float | None

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


def final_flour(total_flour: float, starter: Starter, second_flour: float | None = None) -> float:
    final_flour: float = total_flour - starter.flour
    return final_flour


def taste_flour(final_flour: float, taste_flour: float) -> float:
    taste_flour = (final_flour * taste_flour) / 100.0
    return taste_flour


def water(total_flour: float, hydration_percent: float, starter: Starter) -> float:
    water = total_flour * hydration_percent / 100 - starter.water
    return water


def salt(total_flour: float, salt_percent: float) -> float:
    salt = total_flour * salt_percent / 100
    return salt


def calculate(
    target_weight, hydration_pct, salt_pct, starter_pct, starter_hydration, taste_flour_pct
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
    _taste_flour = taste_flour(_final_flour, taste_flour_pct)
    if _taste_flour:
        _final_flour = _final_flour - _taste_flour
        recipe: RecipieGrams = RecipieGrams(
            flour=_final_flour,
            water=_water,
            starter=_starter.combined,
            salt=_salt,
            taste_flour=_taste_flour,
        )
    else:
        recipe = RecipieGrams(
            flour=_final_flour, water=_water, starter=_starter.combined, salt=_salt
        )
    return recipe
