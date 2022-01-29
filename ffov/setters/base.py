import typing as t
from abc import abstractmethod, ABC


class FovSetter(ABC):
    """Abstract fov setter

    :param gamepath: Path to game root folder.
    """

    #: Registry of fov setters
    _registry: t.Dict[str, "FovSetter"] = {}

    def __init__(self, gamepath: str):
        self.gamepath: str = gamepath

    def __init_subclass__(cls, abstract=False, **kwargs):
        if not abstract:
            cls._registry[getattr(cls, "exe", cls.__name__)] = cls
    
    @classmethod
    def getsetter(cls, name: str) -> t.Optional["FovSetter"]:
        return cls._registry.get(name)
    
    @property
    @abstractmethod
    def exe(self) -> str:
        """str: name of game executable"""
        pass

    @property
    @abstractmethod
    def ini(self) -> str:
        """str: name of game config"""
        pass

    @abstractmethod
    def getfovs(self) -> t.Tuple[float, float, float]:
        pass
    
    @abstractmethod
    def setfovs(
        self,
        fov: t.Union[int, float],
        pipfov: t.Union[int, float],
        termfov: t.Union[int, float]
    ) -> t.Tuple[bool, t.Optional[str]]:
        """Set field of view

        :param fov: Field of view value to set.
        :param pipfov: PipBoy field of view to set.
        :param termfov: Terminal field of view to set.
        :returns: Operation status and error message.
        """
        pass
