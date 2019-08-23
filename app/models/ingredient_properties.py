""" Ingredient Properties module """


class IngredientType(object):
    """ Ingredient type enum """

    POTION = 'Potion'
    POISON = 'Poison'
    ENCHANTMENT = 'Enchantment'

    _duration_multiplier = {
        POTION: 1,
        POISON: 1.1,
        ENCHANTMENT: 1.3
    }

    @classmethod
    def duration_multiplier(cls, t):
        return cls._duration_multiplier.get(t, 1)


class IngredientRarity(object):
    """ Ingredient rarity enum """

    COMMON = 'Common'
    UNCOMMON = 'Uncommon'
    RARE = 'Rare'
    VERY_RARE = 'Very Rare'

    _duration_multiplier = {
        COMMON: .7,
        UNCOMMON: 1,
        RARE: 1.4,
        VERY_RARE: 1.9
    }

    @classmethod
    def duration_multiplier(cls, r):
        return cls._duration_multiplier.get(r, 1)


class IngredientFunction(object):
    """ Ingredient function enum """

    EFFECT = 'Effect'
    MODIFIER = 'Modifier'


class IngredientTerrain(object):
    """ Ingredient terrain enum """

    MOST = 'Most Terrain'
    ARCTIC = 'Arctic'
    COASTAL = 'Coastal'
    DESERT = 'Desert'
    FOREST = 'Forest'
    GRASSLAND = 'Grassland'
    HILL = 'Hill'
    MOUNTAIN = 'Mountain'
    SWAMP = 'Swamp'
    UNDERDARK = 'Underdark'
    UNDERWATER = 'Underwater'
    SPECIAL = 'Special'
