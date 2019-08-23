""" Alchemy Attempt module """


from app.exceptions.errors import *
from app.objects.ingredients import Bloodgrass, ElementalWater
from app.models.ingredient_properties import IngredientType, IngredientFunction, IngredientRarity


class AlchemyAttempt(object):
    """ Represents an Alchemy attempt """

    def __init__(self):
        self._type = None
        self._max_effects = 1
        self._effects = []
        self._max_modifiers = 3
        self._modifiers = []
        self._duration_multiplier = .5

    def __str__(self):
        return ', '.join([str(i) for i in self._effects + self._modifiers])

    @property
    def type(self):
        return self._type

    @property
    def ingredients(self):
        return self._effects + self._modifiers

    def iter(self):
        for i in self.ingredients:
            yield i

    @property
    def final_dc(self):
        """ Calculates the final Alchemy DC """
        return sum([i.dc for i in self.iter()])

    @property
    def craft_duration(self):
        """ Calculates the final craft duration """
        '''calc = lambda v: max(round(v * 2) / 4, .5)
        return calc(int(calc(self.final_dc) + .5))'''
        secs = self.final_dc * 60 * 60 * IngredientType.duration_multiplier(self._type)
        return max(secs - (secs % 3600), 1800)

    def add_ingredient(self, ingredient):
        """ Add an ingredient. """
        if ingredient.type[0] == IngredientType.ENCHANTMENT:
            self._add_enchantment_ingredient(ingredient)
        else:
            self._add_normal_ingredient(ingredient)
        self._update_type()

    def _add_enchantment_ingredient(self, ingredient):
        if ingredient.id == ElementalWater().id:
            self._add_effect(ingredient)
        else:
            self._add_modifier(ingredient)

    def _add_normal_ingredient(self, ingredient):
        if ingredient.function == IngredientFunction.EFFECT:
            self._add_effect(ingredient)
        else:
            self._add_modifier(ingredient)

    def _add_effect(self, effect):
        if effect.id == Bloodgrass().id:
            self._max_effects = 2
        if self._type == IngredientType.POISON and effect.is_special:
            self._max_effects = 2
        if len(self._effects) >= self._max_effects:
            s = '' if self._max_effects == 1 else 's'
            t = self._type if self._type else effect.type[0]
            raise TooManyIngredientsError(f'Only {self._max_effects} base ingredient{s} can be used for {t}s.')
        if not self._effects:
            self._type = effect.type[0]
        if self._type not in effect.type:
            raise IncorrectIngredientsError(f'Cannot add a {effect.type[0]} ingredient ({effect.name}) to a {self._type} concoction.')
        self._effects.append(effect)

    def _add_modifier(self, modifier):
        if len(self._modifiers) >= self._max_modifiers:
            s = '' if self._max_modifiers == 1 else 's'
            t = self._type if self._type else modifier.type[0]
            raise TooManyIngredientsError(f'Only {self._max_modifiers} additional ingredient{s} can be used for {t}s.')
        if self._type not in modifier.type:
            raise IncorrectIngredientsError(f'Cannot add a {modifier.type[0]} ingredient ({modifier.name}) to a {self._type} concoction.')
        self._modifiers.append(modifier)

    def _update_type(self):
        if self._effects:
            self._type = self._effects[0].type[0]
        elif self._modifiers:
            self._type = self._modifiers[0].type[0]
        else:
            return
        self._max_modifiers = 1 if self._type == IngredientType.ENCHANTMENT else 3
