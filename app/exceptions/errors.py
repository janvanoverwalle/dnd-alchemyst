""" Errors module"""


class TooManyIngredientsError(Exception):
    """ Raised when attempting to add too many ingredients """
    pass


class IncorrectIngredientsError(Exception):
    """ Raised when attempting to add incorrect ingredients """
    pass
