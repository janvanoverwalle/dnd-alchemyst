""" Test Class for Enchantments """

from app.common.decorators import raises

from app.exceptions.errors import TooManyIngredientsError, IncorrectIngredientsError

from app.data.ingredient_properties import *
from app.objects.ingredients import *


class TestEnchantments:
    def test_valid_enchantment_final_dc(self, complete_enchantment):
        expected_dc = 5
        actual_dc = complete_enchantment.final_dc

        error_msg = f'Expected the final Alchemy DC to be {expected_dc}, was instead {actual_dc}'
        assert actual_dc == expected_dc, error_msg

    def test_valid_enchantment_type(self, complete_enchantment):
        expected_type = IngredientType.ENCHANTMENT
        actual_type = complete_enchantment.type

        error_msg = f'Expected the concoction type to be {expected_type}, was instead {actual_type}'
        assert actual_type == expected_type, error_msg

    @raises(TooManyIngredientsError)
    def test_invalid_enchantment_two_effects(self, base_enchantment):
        base_enchantment.add_ingredient(ElementalWater())

    @raises(TooManyIngredientsError)
    def test_invalid_enchantment_too_many_ingredients(self, complete_enchantment):
        complete_enchantment.add_ingredient(ScilliaBeans())

    @raises(IncorrectIngredientsError)
    def test_invalid_enchantment_incorrect_ingredient_potion(self, base_enchantment):
        base_enchantment.add_ingredient(MilkweedSeeds())  # Incorrect (Potion) ingredient

    @raises(IncorrectIngredientsError)
    def test_invalid_enchantment_incorrect_ingredient_poison(self, base_enchantment):
        base_enchantment.add_ingredient(SpineflowerBerries())  # Incorrect (Poison) ingredient
