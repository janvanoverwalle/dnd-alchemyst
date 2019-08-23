""" Alchemyst module """

import time

from app.objects.ingredients import *
from app.objects.alchemy_attempt import AlchemyAttempt
from app.models.ingredient_properties import IngredientRarity


def format_duration(duration):
    h = int(duration / 3600)
    duration -= h * 3600
    m = int(duration / 60)
    duration -= m * 60
    s = int(duration)
    format_unit = lambda v, u: f'{v}{u}' if v else ''
    return format_unit(h, 'h') + format_unit(m, 'm') + format_unit(s, 's')


def print_concoction(concoction):
    print(f'Ingredients: {concoction}')
    print(f'Final Alchemy DC: {concoction.final_dc:+}')
    print(f'Craft Duration: {format_duration(concoction.craft_duration)}')
    print()


def potion():
    """ Creates a potion """

    attempt = AlchemyAttempt()
    attempt.add_ingredient(WildSageroot())
    #attempt.add_ingredient(MilkweedSeeds())  # +2
    #attempt.add_ingredient(DriedEphedra())  # +2
    attempt.add_ingredient(LavenderSprig())  # -2
    #attempt.add_ingredient(ChromusSlime())  # +4

    return attempt

def poison():
    """ Creates a poison """

    attempt = AlchemyAttempt()
    attempt.add_ingredient(WyrmtonguePetals())  # +0
    attempt.add_ingredient(BasiliskBreath())  # +5
    attempt.add_ingredient(FrozenSeedlings())  # +4
    attempt.add_ingredient(ChromusSlime())  # +4

    return attempt


def enchantment():
    """ Creates an enchantment """

    attempt = AlchemyAttempt()
    attempt.add_ingredient(ElementalWater())  # +3
    attempt.add_ingredient(WispStalks())  # +5

    return attempt


def main():
    """ Main function """

    concoction = potion()
    print_concoction(concoction)

    concoction = poison()
    print_concoction(concoction)

    concoction = enchantment()
    print_concoction(concoction)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'{e}') 
