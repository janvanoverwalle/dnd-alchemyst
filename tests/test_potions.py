""" Test Class for Potions """

from app.common.decorators import raises

from app.exceptions.errors import TooManyIngredientsError, IncorrectIngredientsError

from app.models.ingredient_properties import *
from app.objects.ingredients import *


class TestPotions:
    def test_valid_potion_final_dc(self, complete_potion):
        expected_dc = 2
        actual_dc = complete_potion.final_dc

        error_msg = f'Expected the final Alchemy DC to be {expected_dc}, was instead {actual_dc}'
        assert actual_dc == expected_dc, error_msg

    def test_valid_potion_type(self, complete_potion):
        expected_type = IngredientType.POTION
        actual_type = complete_potion.type

        error_msg = f'Expected the concoction type to be {expected_type}, was instead {actual_type}'
        assert actual_type == expected_type, error_msg

    def test_valid_potion_two_effects(self, base_potion):
        base_potion.add_ingredient(Bloodgrass())

        expected_ingredients = 2
        actual_ingredients = len(base_potion.ingredients)

        error_msg = (
            f'Expected the concoction to have {expected_ingredients} ingredients, '
            f'was instead {actual_ingredients}'
        )
        assert actual_ingredients == expected_ingredients, error_msg

    def test_valid_potion_special_ingredient(self, base_potion):
        base_potion.add_ingredient(ChromusSlime())

        expected_ingredients = 2
        actual_ingredients = len(base_potion.ingredients)

        error_msg = (
            f'Expected the concoction to have {expected_ingredients} ingredients, '
            f'was instead {actual_ingredients}'
        )
        assert actual_ingredients == expected_ingredients, error_msg

    @raises(TooManyIngredientsError)
    def test_invalid_potion_two_effects(self, base_potion):
        base_potion.add_ingredient(FennelSilk())

    @raises(TooManyIngredientsError)
    def test_invalid_potion_too_many_ingredients(self, complete_potion):
        complete_potion.add_ingredient(GengkoBrush())

    @raises(IncorrectIngredientsError)
    def test_invalid_potion_incorrect_ingredient_poison(self, base_potion):
        base_potion.add_ingredient(SpineflowerBerries())  # Incorrect (Poison) ingredient

    @raises(IncorrectIngredientsError)
    def test_invalid_potion_incorrect_ingredient_enchantment(self, base_potion):
        base_potion.add_ingredient(ArrowRoot())  # Incorrect (Enchantment) ingredient
