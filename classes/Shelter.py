class Shelter(object):
    def __init__(self, name, id, owner, capacity, bedsOccupied):
        self._name = name
        self._id = id
        self._owner = owner
        self._capacity = capacity
        self._bedsOccupied = bedsOccupied

    # def __init__(self, **entries):
    #     self.__dict__.update(entries)

    #
    # GETTERS AND SETTERS
    #
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id


    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, owner):
        self._owner = owner


    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def owner(self, capacity):
        self._capacity = capacity


    @property
    def bedsOccupied(self):
        return self._bedsOccupied

    @bedsOccupied.setter
    def owner(self, bedsOccupied):
        self._bedsOccupied = bedsOccupied






    @staticmethod
    def from_dict(source):
        shelter = Shelter()
        Shelter.__dict__ = source
        return shelter

    # def getCoordinates():
    #     return
    
    # def getMapLink():
    #     return

    
    


    def getFreeBeds(self):
        return self.capacity-self.bedsOccupied

    def to_dict(self):
        shelter = []
        shelter['name'] = this.name
        shelter['id'] = this.id
        shelter['owner'] = this.owner
        shelter['capacity'] = this.capacity
        shelter['bedsOccupied'] = this.bedsOccupied
        return shelter

    def __repr__(self):
        return u'City(name={}, id={}, owner={}, capacity={}, bedsOccupied={})'.format(
            self.name, self.id, self.owner, self.capacity, self.bedsOccupied)
