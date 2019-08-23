""" Alchemyst module """

import time

from app.objects.ingredients import Ingredients
from app.objects.alchemy_attempt import AlchemyAttempt
from app.data.ingredient_properties import IngredientRarity


ALCH_MOD = 3


def format_duration(duration):
    h = int(duration / 3600)
    duration -= h * 3600
    m = int(duration / 60)
    duration -= m * 60
    s = int(duration)
    format_unit = lambda v, u: f'{v}{u}' if v else ''
    return format_unit(h, 'h') + format_unit(m, 'm') + format_unit(s, 's')


def print_concoction(concoction):
    print(f'Concoction Type: {concoction.type}')
    print(f'Ingredients: {concoction}')
    print(f'Alchemy modifier: {ALCH_MOD:+}')
    print(f'Final Alchemy DC: {concoction.final_alchemy_dc}')
    print(f'Craft Duration: {format_duration(concoction.craft_duration)}')
    print(f'Effects:')
    #print(f'{concoction.final_effect}')
    for elem in concoction.details:
        print('* {0}'.format(elem))
    print()


def potion():
    """ Creates a potion """

    attempt = AlchemyAttempt(ALCH_MOD)
    #attempt.add_ingredient(Ingredients.BLOODGRASS)  # +0
    attempt.add_ingredient(Ingredients.CHROMUS_SLIME)  # +4
    attempt.add_ingredient(Ingredients.DRIED_EPHEDRA)  # +2
    #attempt.add_ingredient(Ingredients.EMETIC_WAX)  # +1
    #attempt.add_ingredient(Ingredients.FENNEL_SILK)  # +2
    #attempt.add_ingredient(Ingredients.GENGKO_BRUSH)  # +2
    #attempt.add_ingredient(Ingredients.HYANCINTH_NECTAR)  # +1
    #attempt.add_ingredient(Ingredients.LAVENDER_SPRIG)  # -2
    attempt.add_ingredient(Ingredients.MANDRAKE_ROOT)  # +0
    attempt.add_ingredient(Ingredients.MILKWEED_SEEDS)  # +2
    #attempt.add_ingredient(Ingredients.WILD_SAGEROOT)  # +0

    attempt.brew()
    return attempt

def poison():
    """ Creates a poison """

    attempt = AlchemyAttempt(ALCH_MOD)
    attempt.add_ingredient(Ingredients.WYRMTONGUE_PETALS)  # +0
    #attempt.add_ingredient(Ingredients.ARCTIC_CREEPER)  # +2
    #attempt.add_ingredient(Ingredients.AMANITA_CAP)  # +1
    attempt.add_ingredient(Ingredients.BASILISK_BREATH)  # +5
    #attempt.add_ingredient(Ingredients.CACTUS_JUICE)  # +2
    attempt.add_ingredient(Ingredients.CHROMUS_SLIME)  # +4
    #attempt.add_ingredient(Ingredients.DRAKUS_FLOWER)  # +2
    #attempt.add_ingredient(Ingredients.EMETIC_WAX)  # +2
    attempt.add_ingredient(Ingredients.FROZEN_SEEDLINGS)  # +4
    #attempt.add_ingredient(Ingredients.HARRADA_LEAF)  # +1
    #attempt.add_ingredient(Ingredients.LAVENDER_SPRIG)  # -2
    #attempt.add_ingredient(Ingredients.QUICKSILVER_LICHEN)  # +3
    #attempt.add_ingredient(Ingredients.RADIANT_SYNTHSEED)  # +2
    #attempt.add_ingredient(Ingredients.SPINEFLOWER_BERRIES)  # +3

    attempt.brew()
    return attempt


def enchantment():
    """ Creates an enchantment """

    attempt = AlchemyAttempt(ALCH_MOD)
    attempt.add_ingredient(Ingredients.ELEMENTAL_WATER)  # +3
    #attempt.add_ingredient(Ingredients.ARROW_ROOT)  # +2
    #attempt.add_ingredient(Ingredients.BLUE_TOADSHADE)  # +3
    #attempt.add_ingredient(Ingredients.COSMOS_GLOND)  # +3
    #attempt.add_ingredient(Ingredients.DEVILS_BLOODLEAF)  # +5
    #attempt.add_ingredient(Ingredients.FIENDS_IVY)  # +4
    #attempt.add_ingredient(Ingredients.HYDRATHISTLE)  # +2
    #attempt.add_ingredient(Ingredients.IRONWOOD_HEART)  # +3
    #attempt.add_ingredient(Ingredients.LUMINOUS_CAP_DUST)  # +4
    #attempt.add_ingredient(Ingredients.MORTFLESH_POWDER)  # +5
    #attempt.add_ingredient(Ingredients.NIGHTSHADE_BERRIES)  # +3
    #attempt.add_ingredient(Ingredients.PRIMORDIAL_BALM)  # +4
    #attempt.add_ingredient(Ingredients.ROCK_VINE)  # +4
    #attempt.add_ingredient(Ingredients.SCILLIA_BEANS)  # +1
    #attempt.add_ingredient(Ingredients.SILVER_HIBISCUS)  # +4
    attempt.add_ingredient(Ingredients.TAIL_LEAF)  # +5
    #attempt.add_ingredient(Ingredients.VERDANT_NETTLE)  # +2
    #attempt.add_ingredient(Ingredients.VOIDROOT)  # +5
    #attempt.add_ingredient(Ingredients.WISP_STALKS)  # +5
    #attempt.add_ingredient(Ingredients.WRACKWORT_BULBS)  # +4

    attempt.brew()
    return attempt


def main():
    """ Main function """

    try:
        concoction = potion()
        print_concoction(concoction)
    except Exception as e:
        print(f'{e}')
        print()

    try:
        concoction = poison()
        print_concoction(concoction)
    except Exception as e:
        print(f'{e}')
        print()
    
    try:
        concoction = enchantment()
        print_concoction(concoction)
    except Exception as e:
        print(f'{e}')
        print()


if __name__ == '__main__':
    main()
    """try:
        main()
    except Exception as e:
        print(f'{e}')"""
