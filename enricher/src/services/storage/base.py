from abc import abstractmethod


class BaseStorage:
    @abstractmethod
    async def insert(self, *args, **kwargs):
        raise NotImplementedError('Need for implementation!')

    @abstractmethod
    async def select(self, *args, **kwargs):
        raise NotImplementedError('Need for implementation!')

    @abstractmethod
    async def view_all(self, *args, **kwargs):
        raise NotImplementedError('Need for implementation!')

    @abstractmethod
    async def count(self, *args, **kwargs):
        raise NotImplementedError('Need for implementation!')
