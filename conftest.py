import pytest

from app.objects.ingredients import *
from app.objects.alchemy_attempt import AlchemyAttempt


@pytest.fixture
def base_potion(request):
    attempt = AlchemyAttempt()
    attempt.add_ingredient(WildSageroot())
    return attempt


@pytest.fixture
def base_poison(request):
    attempt = AlchemyAttempt()
    attempt.add_ingredient(WyrmtonguePetals())
    return attempt


@pytest.fixture
def base_enchantment(request):
    attempt = AlchemyAttempt()
    attempt.add_ingredient(ElementalWater())
    return attempt


@pytest.fixture
def complete_potion(request):
    attempt = AlchemyAttempt()
    attempt.add_ingredient(WildSageroot())
    attempt.add_ingredient(MilkweedSeeds())
    attempt.add_ingredient(DriedEphedra())
    attempt.add_ingredient(LavenderSprig())
    return attempt


@pytest.fixture
def complete_poison(request):
    attempt = AlchemyAttempt()
    attempt.add_ingredient(WyrmtonguePetals())
    attempt.add_ingredient(SpineflowerBerries())
    attempt.add_ingredient(QuicksilverLichen())
    attempt.add_ingredient(HarradaLeaf())
    return attempt


@pytest.fixture
def complete_enchantment(request):
    attempt = AlchemyAttempt()
    attempt.add_ingredient(ElementalWater())
    attempt.add_ingredient(ArrowRoot())
    return attempt
