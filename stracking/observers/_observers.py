
class SObservable:
    """Interface for data processing class

    The observable class can notify the observers for progress

    """
    def __init__(self):
        self._observers = list()

    def add_observer(self, observer):
        """Add an observer

        Parameters
        ----------
        observer: SObserver
            Observer class

        """
        self._observers.append(observer)

    def notify(self, message):
        """Notify progress to observers

        Parameters
        ----------
        message: str
            Progress message

        """
        for obs in self._observers:
            obs.notify(message)

    def progress(self, value):
        """Notify progress to observers

        Parameters
        ----------
        value: int
            Progress value in [0, 100]

        """
        for obs in self._observers:
            obs.progress(value)


class SObserver:
    """Interface of observer to notify progress

    An observer must implement the progress and message

    """
    def __init__(self):
        pass

    def notify(self, message):
        """Notify a progress message

        Parameters
        ----------
        message: str
            Progress message

        """
        raise Exception('SObserver is abstract')

    def progress(self, value):
        """Notify progress value

        Parameters
        ----------
        value: int
            Progress value in [0, 100]

        """
        raise Exception('SObserver is abstract')


class SObserverConsole(SObserver):
    """print message and progress to console"""
    def __init__(self):
        super().__init__()
        pass

    def notify(self, message):
        print(message)

    def progress(self, value):
        print('progress:', value, '%')
