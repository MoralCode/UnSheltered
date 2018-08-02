class Shelter(object):
    # def __init__(self, name, id, owner, capacity, bedsOccupied):
    #     self.name = name
    #     self.id = id
    #     self.owner = owner
    #     self.capacity = capacity
    #     self.bedsOccupied = bedsOccupied

    def __init__(self, **entries):
        self.__dict__.update(entries)

    #
    # GETTERS AND SETTERS
    #
    
    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        self.name = name


    @property
    def id(self):
        return self.id

    @id.setter
    def id(self, id):
        self.id = id


    @property
    def owner(self):
        return self.owner

    @owner.setter
    def owner(self, owner):
        self.owner = owner


    @property
    def capacity(self):
        return self.capacity

    @capacity.setter
    def owner(self, capacity):
        self.capacity = capacity


    @property
    def bedsOccupied(self):
        return self.bedsOccupied

    @bedsOccupied.setter
    def owner(self, bedsOccupied):
        self.bedsOccupied = bedsOccupied






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
