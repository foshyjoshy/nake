from logging import debug
from abc import ABC

class Registry():
    """ A class to register classes """

    CLASS_NAME = "class_name"

    registry = {}

    def __new__(cls, class_name, *args, **kwargs):
        if class_name is None:
            return
        else:
            return cls.getInitialized(class_name, *args, **kwargs)

    @classmethod
    def registrySubclass(cls):
        return

    @classmethod
    def isClassRegistered(cls, cls_):
        """ Checks if the cls_ is registered"""
        return cls_ in list(cls.registry.values())

    @classmethod
    def isNameRegistered(cls, name):
        """" Checks if a name is in the registry"""
        return name in cls.registry

    @classmethod
    def isObjectRegistered(cls, obj):
        """ Checks if this objects class has been registered"""
        for i in list(cls.registry.values()):
            if isinstance(obj, i):
                return True
        else: return False

    @classmethod
    def register(cls, act):
        """" Register an activation"""
        if cls.registrySubclass() is not None:
            if not issubclass(act, cls.registrySubclass()):
                raise Exception("Unable to register {}. \
                    Not a subclass of {}".format(act, cls.registrySubclas()))
        if cls.isNameRegistered(act.getClassName()):
            raise Exception("Unable to register {}. \
                {} is already registered".format(act, act.getClassName()))

        debug("Registered class {} with name {}".format(act, act.getClassName()))
        cls.registry[act.getClassName()] = act

    @classmethod
    def get(cls, name, value=None):
        """ Returns registered cls with name"""
        return cls.registry.get(name, value)

    @classmethod
    def getInitialized(cls, class_name, *args, **kwargs):
        """ Returns registered initialized activation with name"""
        if cls.isNameRegistered(class_name):
            return cls.get(class_name)(*args, **kwargs)
        else:
            raise Exception("Nothing has been registered \
                with name \"{}\". Available {}".format(class_name, cls.registry))

    @classmethod
    def registeredNames(self):
        """ Returns the registry keys"""
        return list(self.registry.keys())

    @classmethod
    def registeredClasses(self):
        """ Returns the registry classes"""
        return list(self.registry.values())




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
    def getClassName(cls):
        """ Returns the name of the item"""
        return cls.__name__.lower()

    def __getstate__(self):
        """ Returns the state of this object """
        return {Registry.CLASS_NAME : self.getClassName()}
