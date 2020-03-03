from logging import debug
import consts
from abc import ABC


class Registry():
    """ A class to register classes """

    registry = {}

    def __new__(cls, name, *args, **kwargs):
        return cls.getInitialized(name, *args, **kwargs)

    @classmethod
    def registrySubclass(cls):
        return

    @classmethod
    def isRegistered(cls, obj):
        """ Checks if the obj is registered"""
        return obj in cls.registry.items()

    @classmethod
    def isNameRegistered(cls, name):
        """" Checks if a name is in the registry"""
        return name in cls.registry

    @classmethod
    def register(cls, act):
        """" Register an activation"""
        if cls.registrySubclass() is not None:
            if not issubclass(act, cls.registrySubclass()):
                raise Exception("Unable to register {}. \
                    Not a subclass of {}".format(act, cls.registrySubclas()))
        if cls.isNameRegistered(act.getItemName()):
            raise Exception("Unable to register {}. \
                {} is already registered".format(act, act.getItemName()))

        debug("Registered class {} with name {}".format(act, act.getItemName()))
        cls.registry[act.getItemName()] = act

    @classmethod
    def get(cls, name, value=None):
        """ Returns registered cls with name"""
        return cls.registry.get(name, value)

    @classmethod
    def getInitialized(cls, name, *args, **kwargs):
        """ Returns registered initialized activation with name"""
        if cls.isNameRegistered(name):
            return cls.get(name)(*args, **kwargs)
        else:
            raise Exception("Nothing has been registered \
                with name \"{}\". Available {}".format(name, cls._registry))

    @classmethod
    def registeredNames(self):
        """ Returns the registry keys"""
        return list(self.registry.keys())




class RegistryItemBase(ABC):
    """" Base class for Registry item"""

    REGISTRY, _REGISTRY = None, None

    def __init_subclass__(cls, **kwargs):
        if cls._REGISTRY is None:
            if cls.REGISTRY is None:
                raise Exception("Registry not set. Unable to register {}".format(cls))
            cls._REGISTRY = cls.REGISTRY
            super().__init_subclass__(**kwargs)
        else:
            super().__init_subclass__(**kwargs)
            cls._REGISTRY.register(cls)


    @classmethod
    def getItemName(cls):
        """ Returns the name of the item"""
        return cls.__name__.lower()

    def getState(self):
        """ Returns the state of this object """
        return {consts.NAME : self.getItemName()}
