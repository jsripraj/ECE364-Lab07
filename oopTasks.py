from enum import Enum
import re
import random
import uuid

# Level = Enum('Level', 'freshman, sophomore, junior, senior')
class Level(Enum):
    freshman = 1
    sophomore = 2
    junior = 3
    senior = 4
class Student:
    def __init__(self, ID, firstName, lastName, level):
        self.ID = str(ID)
        self.firstName = firstName
        self.lastName = lastName
        if isinstance(level, Level):
            self.level = level
        else:
            raise TypeError("The argument must be an instance of the 'Level' Enum.")
    def __str__(self):
        return "{}, {} {}, {}".format(self.ID, self.firstName, self.lastName, self.level.name.title())
class Circuit:
    def __init__(self, ID, resistors, capacitors, inductors, transistors):
        self.ID = str(ID)
        invalid = []
        for resistor in resistors:
            if 'R' not in resistor:
                invalid.append(resistor)
        if invalid:
            raise ValueError("The resistors' list contain invalid components: {}".format(invalid))
        self.resistors = resistors
        for capacitor in capacitors:
            if 'C' not in capacitor:
                invalid.append(capacitor)
        if invalid:
            raise ValueError("The capacitors' list contain invalid components: {}".format(invalid))
        self.capacitors = capacitors
        for inductor in inductors:
            if 'L' not in inductor:
                invalid.append(inductor)
        if invalid:
            raise ValueError("The inductors' list contain invalid components: {}".format(invalid))
        self.inductors = inductors
        for transistor in transistors:
            if 'T' not in transistor:
                invalid.append(transistor)
        if invalid:
            raise ValueError("The transistors' list contain invalid components: {}".format(invalid))
        self.transistors = transistors
    def __str__(self):
        return "{}: (R = {:02}, C = {:02}, L = {:02}, T = {:02})".format(self.ID, len(self.resistors), len(self.capacitors), len(self.inductors), len(self.transistors))
    def getDetails(self):
        return "{}: {}, {}, {}, {}".format(self.ID, ', '.join(sorted(self.resistors)), ', '.join(sorted(self.capacitors)), ', '.join(sorted(self.inductors)), ', '.join(sorted(self.transistors)))
    def __contains__(self, component):
        if not isinstance(component, str):
            raise TypeError("Component must be formatted as a string.")
        if not re.match('[RCLT]', component):
            raise ValueError("Component is of unknown type.")
        if component in self.resistors or component in self.capacitors or component in self.inductors or component in self.transistors:
            return True
        return False
    def __add__(self, component):
        # Circuit + component
        if not isinstance(component, Circuit):
            if not isinstance(component, str):
                raise TypeError("Components must be formatted as strings and "
                                "circuits must be instances of the circuit class.")
            if not re.match('[RCLT]', component):
                raise ValueError("Component is of unknown type.")
            if component not in self:
                if re.match('R', component):
                    self.resistors.append(component)
                elif re.match('C', component):
                    self.capacitors.append(component)
                elif re.match('L', component):
                    self.inductors.append(component)
                elif re.match('T', component):
                    self.transistors.append(component)
            return self
        # Circuit1 + Circuit2
        else:
            newID = str(random.randint(10000, 99999))
            newResistors = list(set(self.resistors + component.resistors))
            newCapacitors = list(set(self.capacitors + component.capacitors))
            newInductors = list(set(self.inductors + component.inductors))
            newTransistors = list(set(self.transistors + component.transistors))
            return Circuit(newID, newResistors, newCapacitors, newInductors, newTransistors)
    #
    # def __radd__(self, component):
    #     return self.__add__(component)
    def __sub__(self, component):
        if not isinstance(component, str):
            raise TypeError("Component must be formatted as a string.");
        if not re.match('[RCLT]', component):
            raise ValueError("Component is of unkown type.")
        if component in self:
            if re.match('R', component):
                self.resistors.remove(component)
            elif re.match('C', component):
                self.capacitors.remove(component)
            elif re.match('L', component):
                self.inductors.remove(component)
            elif re.match('T', component):
                self.transistors.remove(component)
        return self
class Project:
    def __init__(self, ID, participants, circuits):
        self.ID = str(ID)
        for participant, circuit in zip(participants, circuits):
            if not participants:
                raise ValueError("Participants list cannot be empty.")
            if not circuits:
                raise ValueError("Circuits list cannot be empty.")
            if not isinstance(participant, Student):
                raise ValueError("All participants must be of the Student class.")
            if not isinstance(circuit, Circuit):
                raise ValueError("All circuits must be of the Circuit class")
        self.participants = participants
        self.circuits = circuits
    def __str__(self):
        return "{}: {:02} Circuits, {:02} Participants".format(self.ID, len(self.circuits), len(self.participants))
    def getDetails(self):
        return "{}\n\nParticipants:\n{}\n\nCircuits:\n{}\n"\
            .format(self.ID, "\n".join([str(participant) for participant in sorted(self.participants, key=lambda x: x.ID)]),
                    "\n".join([circuit.getDetails() for circuit in sorted(self.circuits, key=lambda x: x.ID)]))
    def __contains__(self, item):
        if isinstance(item, str):
            if not re.match('[RCLT]', item):
                raise ValueError("Component is of unknown type.")
            for circuit in self.circuits:
                if item in circuit:
                    return True
            return False
        elif isinstance(item, Circuit):
            if item in self.circuits:
                return True
            return False
        elif isinstance(item, Student):
            if item in self.participants:
                return True
            return False
        else:
            raise TypeError("To check for membership, item must belong to string, Circuit, or Student class.")
    def __add__(self, other):
        if isinstance(other, Circuit):
            if other not in self.circuits:
                self.circuits.append(other)
            return self
        elif isinstance(other, Student):
            if other not in self.participants:
                self.participants.append(other)
            return self
        else:
            raise TypeError("Item to be added must be of the Circuit or Student class.")
    def __sub__(self, other):
        if isinstance(other, Circuit):
            if other in self.circuits:
                self.circuits.remove(other)
            return self
        elif isinstance(other, Student):
            if other in self.participants:
                self.participants.remove(other)
            return self
        else:
            raise TypeError("Item to be removed must be of the Circuit or Student class.")
class Capstone(Project):
    def __init__(self, ID, participants, circuits):
        Project.__init__(self, ID, participants, circuits)
        for participant in self.participants:
            if not participant.level == Level.senior:
                raise ValueError("All participating students must be seniors.")
    def __add__(self, other):
        if not other.level == Level.senior:
            raise ValueError("Student to be added must be a senior.")
        Project.__add__(self, other)
if __name__ == "__main__":
    s = Student('00283-56512', 'Joe', 'Smith', Level.senior)
    s1 = Student('26532-65398', 'Katrina', 'Ryan', Level.senior)
    s2 = Student('36598-45210', 'Chase', 'Chad', Level.senior)
    c1 = Circuit(99887, ['R206.298','R436.943'], ['C261.054', 'C194.315', 'C668.027'], ['L49.234'], ['T663.350'])
    c2 = Circuit(65465, ['R526.365', 'R125.269', 'R458.256'], ['C526.368', 'C548.222'], ['L542.258'], ['T542.369'])
    cNew = c1 + c2
    print('c1: {}'.format(c1.getDetails()))
    print('c2: {}'.format(c2.getDetails()))
    print('cNew: {}'.format(cNew.getDetails()))
    # 'T999.999' + cNew + 1
    # print('cNew: {}'.format(cNew.getDetails()))
    # p = Project(uuid.uuid1(), [s, s1], [c1, c2])
    # print(p.getDetails())
    # p + cNew
    # print(p.getDetails())
    # p + s2
    # print(p.getDetails())
    # p - cNew
    # # print(p.getDetails())
    # p - s2
    # # print(p.getDetails())
    # c = Capstone(uuid.uuid1(), [s, s1], [c1, c2])
    # print(c.getDetails())
    # c + s2
    # print(c.getDetails())