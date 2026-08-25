class Node:
    def __init__(self, number: int):
        if number < 0:
            raise ValueError("Node number must be a non-negative integer.")

        self.number = number
        self.index = None
        self._voltage = None
        self._connections = []

    def add_element(self, element):
        # TODO: Add validation to ensure the element is a valid circuit element
        self._connections.append(element)

    @property
    def connections(self):
        return self._connections

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        if (
            not isinstance(voltage, (int, float))
            or voltage is True
            or voltage is False
        ):
            raise TypeError("voltage must be a non-negative int or float")

        self._voltage = voltage

    def __repr__(self):
        return f"Node(number={self.number}, voltage={self._voltage})"

    def __eq__(self, value):
        return self.number == value
