from logging import debug
import consts


class Registry():
    """ A class to register classes """

    _registry = {}

    def __new__(cls, **kwargs):
        return cls.getInitialized(kwargs.pop(consts.NAME,None), **kwargs)

    @classmethod
    def registrySubclass(cls):
        return

    @classmethod
    def isRegistered(cls, obj):
        """ Checks if the obj is registered"""
        return obj in cls._registry.items()

    @classmethod
    def isNameRegistered(cls, name):
        """" Checks if a name is in the registry"""
        return name in cls._registry

    @classmethod
    def register(cls, act):
        """" Register an activation"""
        if cls.registrySubclass() is not None:
            if not issubclass(act, cls.registrySubclass()):
                raise Exception("Unable to register {}. \
                    Not a subclass of {}".format(act, cls.registrySubclas()))
        if cls.isNameRegistered(act.getName()):
            raise Exception("Unable to register {}. \
                {} is already registered".format(act, act.getName()))

        debug("Registered class {} with name {}".format(act, act.getName()))
        cls._registry[act.getName()] = act

    @classmethod
    def get(cls, name, value=None):
        """ Returns registered cls with name"""
        return cls._registry.get(name, value)

    @classmethod
    def getInitialized(cls, name, *args, **kwargs):
        """ Returns registered initialized activation with name"""
        if cls.isNameRegistered(name):
            return cls.get(name)(*args, **kwargs)
        else:
            Exception("Nothing has been registered with name \"{}\"".format(name))