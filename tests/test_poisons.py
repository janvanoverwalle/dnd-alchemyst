""" Test Class for Poisons """

from app.common.decorators import raises

from app.exceptions.errors import TooManyIngredientsError, IncorrectIngredientsError

from app.models.ingredient_properties import *
from app.objects.ingredients import *


class TestPoisons:
    def test_valid_poison_final_dc(self, complete_poison):
        expected_dc = 7
        actual_dc = complete_poison.final_dc

        error_msg = f'Expected the final Alchemy DC to be {expected_dc}, was instead {actual_dc}'
        assert actual_dc == expected_dc, error_msg

    def test_valid_poison_type(self, complete_poison):
        expected_type = IngredientType.POISON
        actual_type = complete_poison.type

        error_msg = f'Expected the concoction type to be {expected_type}, was instead {actual_type}'
        assert actual_type == expected_type, error_msg

    def test_valid_poison_special_ingredient(self, base_poison):
        base_poison.add_ingredient(ChromusSlime())

        expected_ingredients = 2
        actual_ingredients = len(base_poison.ingredients)

        error_msg = (
            f'Expected the concoction to have {expected_ingredients} ingredients, '
            f'was instead {actual_ingredients}'
        )
        assert actual_ingredients == expected_ingredients, error_msg

    def test_valid_poison_special_effect_ingredient(self, base_poison):
        base_poison.add_ingredient(BasiliskBreath())

        expected_ingredients = 2
        actual_ingredients = len(base_poison.ingredients)

        error_msg = (
            f'Expected the concoction to have {expected_ingredients} ingredients, '
            f'was instead {actual_ingredients}'
        )
        assert actual_ingredients == expected_ingredients, error_msg

    @raises(TooManyIngredientsError)
    def test_invalid_potion_two_effects(self, base_potion):
        base_potion.add_ingredient(WyrmtonguePetals())

    @raises(TooManyIngredientsError)
    def test_invalid_poison_too_many_ingredients(self, complete_poison):
        complete_poison.add_ingredient(DrakusFlower())

    @raises(IncorrectIngredientsError)
    def test_invalid_poison_incorrect_ingredient_potion(self, base_poison):
        base_poison.add_ingredient(MilkweedSeeds())  # Incorrect (Potion) ingredient

    @raises(IncorrectIngredientsError)
    def test_invalid_poison_incorrect_ingredient_enchantment(self, base_poison):
        base_poison.add_ingredient(ArrowRoot())  # Incorrect (Enchantment) ingredient
