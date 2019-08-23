""" Alchemy Attempt module """


from app.exceptions.errors import *
from app.objects.ingredients import Ingredients
from app.data.dice import Dice
from app.data.ingredient_properties import IngredientType, IngredientFunction, IngredientRarity


class AlchemyAttempt(object):
    """ Represents an Alchemy attempt """

    def __init__(self, alchemy_modifier=0):
        self._alchemy_modifier = alchemy_modifier
        self._ingredients = []
        self._type = None
        self._max_effects = 1
        self._effects = []
        self._max_modifiers = 3
        self._modifiers = []
        self._duration_multiplier = .5
        self._properties = []

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
    def final_alchemy_dc(self):
        """ Calculates the final Alchemy DC """
        return 10 + self.ingredient_dcs

    @property
    def ingredient_dcs(self):
        return sum([i.dc for i in self.iter()])

    @property
    def craft_duration(self):
        """ Calculates the final craft duration """
        '''calc = lambda v: max(round(v * 2) / 4, .5)
        return calc(int(calc(self.ingredient_dcs) + .5))'''
        secs = self.ingredient_dcs * 3600 * IngredientType.duration_multiplier(self._type)
        return max(secs - (secs % 3600), 1800)

    @property
    def details(self):
        return [i.details for i in self.iter()]

    @property
    def properties(self):
        return [i.property for i in self.iter()]

    @property
    def final_effect(self):
        if self._type == IngredientType.ENCHANTMENT:
            return self.ingredients[-1].property

        fe = {}
        con_saves = []
        conditions = []
        effect_durations = []
        effect_duration_mods = []
        for i in self.iter():
            p = i.property

            if 'effect_dice' in p:
                fe['effect_dice'] = Dice(p['effect_dice'])

            if 'effect_dice' in fe:
                fe['effect_dice'].change_type_by(p.get('increase_dice_type', 0))

            resistance = p.get('resistance')
            if resistance:
                if 'resistances' not in fe:
                    fe['resistances'] = []
                fe['resistances'].append(resistance)

            if 'effect_dice' in fe:
                dice_amount = p.get('dice_amount')
                if dice_amount:
                    op = dice_amount.strip()[0]
                    am = int(dice_amount.strip()[1:])
                    if op == '+':
                        fe['effect_dice'].amount = fe['effect_dice'].amount + am
                    elif op == '-':
                        fe['effect_dice'].amount = fe['effect_dice'].amount - am
                    elif op == ('*'):
                        fe['effect_dice'].amount = fe['effect_dice'].amount * am
                    elif op == ('/'):
                        fe['effect_dice'].amount = fe['effect_dice'].amount / am

            if 'effect_dice' in fe and 'dice_total' in p:
                fe['dice_total'] = p['dice_total']

            duration = p.get('duration')
            if duration:
                if isinstance(duration, str):
                    op = duration.strip()[0]
                    am = float(duration.strip()[1:])
                    if op == '+':
                        effect_duration_mods.append(lambda x: x + am)
                    elif op == '-':
                        effect_duration_mods.append(lambda x: x - am)
                    elif op == ('*'):
                        effect_duration_mods.append(lambda x: x * am)
                    elif op == ('/'):
                        effect_duration_mods.append(lambda x: x / am)
                else:
                    fe['duration'] = duration

            if 'alchemy_modifier' in p:
                self._alchemy_modifier = p['alchemy_modifier']

            if 'damage_type' in p:
                fe['damage_type'] = p['damage_type']

            if 'con_save' in p:
                con_saves.append(p['con_save'])
                save_fail = p.get('save_fail')
                conditions.append(save_fail.get('condition'))
                effect_durations.append(save_fail.get('duration'))

            if 'lethal' in p:
                fe['lethal'] = p['lethal']

            if 'dormant' in p:
                fe['dormant'] = p['dormant']

            if 'speed' in p:
                fe['speed'] = p['speed']

            if 'disadvantage' in p:
                fe['disadvantage'] = p['disadvantage']

            if 'reverse_effect' in p:
                fe['reverse_effect'] = p['reverse_effect']

            if 'delay_effect' in p:
                fe['delay_effect'] = Dice(p['delay_effect'])

        for i, ed in enumerate(effect_durations):
            edm = effect_duration_mods[i] if i < len(effect_duration_mods) else lambda x: x
            fed = edm(ed)
            if 'con_saves' not in fe:
                fe['con_saves'] = []
            fe['con_saves'].append({})
            save_dc = con_saves[i].replace('mod', str(self._alchemy_modifier))
            fe['con_saves'][-1]['dc'] = eval(save_dc)  # I know, I know
            fe['con_saves'][-1]['condition'] = conditions[i]
            fe['con_saves'][-1]['duration'] = int(fed)

        if 'effect_dice' in fe:
            fe['effect_dice'].modifier = self._alchemy_modifier

        return fe

    def add_ingredient(self, ingredient):
        """ Add an ingredient. """
        self._ingredients.append(ingredient)

    def brew(self):
        effects = [i for i in self._ingredients if i.function == IngredientFunction.EFFECT or i.id == Ingredients.ELEMENTAL_WATER.id]
        not_effects = [i for i in self._ingredients if i.function != IngredientFunction.EFFECT and i.id != Ingredients.ELEMENTAL_WATER.id]

        if not effects:
            raise MissingEffectIngredient(f'Every concoction needs at least 1 base ingredient.')

        for i in effects:
            if i.type[0] == IngredientType.ENCHANTMENT:
                self._add_enchantment_ingredient(i)
            else:
                self._add_normal_ingredient(i)
            self._update_type()
            self._properties.append(i.property)

        for i in not_effects:
            if i.type[0] == IngredientType.ENCHANTMENT:
                self._add_enchantment_ingredient(i)
            else:
                self._add_normal_ingredient(i)
            self._update_type()
            self._properties.append(i.property)

    def _add_enchantment_ingredient(self, ingredient):
        if ingredient.id == Ingredients.ELEMENTAL_WATER.id:
            self._add_effect(ingredient)
        else:
            self._add_modifier(ingredient)

    def _add_normal_ingredient(self, ingredient):
        if ingredient.function == IngredientFunction.EFFECT:
            self._add_effect(ingredient)
        else:
            self._add_modifier(ingredient)

    def _add_effect(self, effect):
        if effect.id == Ingredients.BLOODGRASS.id:
            self._max_effects = 2
        if self._type == IngredientType.POISON and effect.is_special:
            self._max_effects = 2
        if len(self._effects) >= self._max_effects:
            s = '' if self._max_effects == 1 else 's'
            t = self._type if self._type else effect.type[0]
            raise TooManyIngredientsError(f'{effect.name} is a base ingredient. Only {self._max_effects} base ingredient{s} can be used for {t}s.')
        if not self._effects:
            self._type = effect.type[0]
        if self._type not in effect.type:
            raise IncorrectIngredientsError(f'Cannot add a {effect.type[0]} ingredient ({effect.name}) to a {self._type} concoction.')
        self._effects.append(effect)

    def _add_modifier(self, modifier):
        if len(self._modifiers) >= self._max_modifiers:
            s = '' if self._max_modifiers == 1 else 's'
            t = self._type if self._type else modifier.type[0]
            raise TooManyIngredientsError(f'{modifier.name} is an additional ingredient. Only {self._max_modifiers} additional ingredient{s} can be used for {t}s.')
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
