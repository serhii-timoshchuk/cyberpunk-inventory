from enum import Enum, EnumMeta


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class ItemCategory(str, Enum, metaclass=MetaEnum):
    WEAPON = 'Weapon'
    CYBERNETIC = 'Cybernetic'
    GADGET = 'Gadget'
