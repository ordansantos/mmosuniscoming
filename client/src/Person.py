

import Character
import PathFind

class Person:
    
    CONST_MAX_WH = 7200
    person_list = []
    
    @staticmethod
    def getNewPlayer(x, y, image = '../characters/sprites/ordan.png', id = len(person_list)):
        if (x > Person.CONST_MAX_WH / 4 or y > Person.CONST_MAX_WH / 4):
            return None
        
        p = Character.Player((x, y), image)
        
        p.setId(id)

        Person.person_list.append(p)
        return p

    
    @staticmethod
    def getNewBot(x, y, image = '../characters/img/blond_man.png', id = len(person_list)):
        if (x > Person.CONST_MAX_WH / 4 or y > Person.CONST_MAX_WH / 4):
            return None
        
        p = Character.Bot((x, y), image)
        
        p.setId(id)

        Person.person_list.append(p)

        return p

    
    @staticmethod
    def getPersonById(p_id):
        
        for p in Person.person_list:
            if (p_id == p.getId()):
                return p
    
        return None

    @staticmethod
    def cmp ((x1, y1), (x2, y2)):
    
        if (y1 < y2):
            return True
        if (y1 == y2):
            if (x1 < x2):
                return True
        return False
    
    @staticmethod
    def getPersons():
        for i in xrange (1, len(Person.person_list)):
            j = i
            while (j > 0 and Person.cmp(Person.person_list[j].getPosition(), Person.person_list[j - 1].getPosition())):
                Person.person_list[j], Person.person_list[j - 1] = Person.person_list[j - 1], Person.person_list[j]
                j -= 1
                    
        return Person.person_list
    
    @staticmethod
    def getMaster():
        
        for p in Person.person_list:
            if (p.id == Person.id_master):
                return p
        return None
    
    @staticmethod
    def setMaster(id_master):
        Person.id_master = id_master

    @staticmethod
    def setDead(person):
        if person in Person.person_list:
            Person.person_list.remove(person)
    
    @staticmethod
    def restartPerson():
        for p in Person.person_list:
            Walls.Walls.freeLocation(p.getPosition())
            p.life = 0
        Person.person_list = []
    