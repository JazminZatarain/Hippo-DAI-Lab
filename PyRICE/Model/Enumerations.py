from enum import Enum


class ModelSpec(Enum):

    def __eq__(self, o: object) -> bool:
        if self.value is o.value:
            return True
        else:
            return False

    Validation_1 = 1
    Validation_2 = 2
    EMA = 3


class WelfareFunction(Enum):
    """
    Social Welfare Functions
    """

    def __eq__(self, o: object) -> bool:
        if self.value is o.value:
            return True
        else:
            return False

    UTILITARIAN = 0
    PRIORITARIAN = 1
    SUFFICIENTARIAN = 2
    EGALITARIAN = 3


class DamageFunction(Enum):
    """
    Damage Functions
    """

    def __eq__(self, o: object) -> bool:
        if self.value is o.value:
            return True
        else:
            return False

    NORDHAUS = 0
    NEWBOLD = 1
    WEITZMAN = 2
