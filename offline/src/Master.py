
class Master:
    
    def __init__(self, idMaster=None, email=None, password=None, killed=None, life=None, dateRecord=None):
        self.idMaster = idMaster
        self.email = email
        self.password = password
        self.killed = killed
        self.life = life
        self.dateRecord = dateRecord
    
    def getMaster(self):
        return (self.idMaster, self.email, self.password, self.killed, self.life, self.dateRecord)
    
    def setMaster(self, master):
        self = master
    
    def toString(self):
        return "Id: " + str(self.idMaster) + "\nEmail: " + str(self.email) + "\nPass: " + str(self.password) + "\nKilled: " + str(self.killed) + "\nLife:" + str(self.life)
    