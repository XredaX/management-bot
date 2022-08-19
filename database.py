import pymongo

passd = "ckZpYU8HGpnc5i9i"
named = "CRYPTO_Sea"

client = pymongo.MongoClient("mongodb+srv://test:"+passd+"@cluster1.9glic.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database(named)

class user():
    def addmembers(collection, fullname, membership, startmembership, endmembership, iduser, spot, future, Owenr):
        collection = db[collection]
        newmember = {"fullname":fullname, "membership":membership, "startmembership":startmembership, "endmembership":endmembership, "iduser":iduser, "spot":spot, "future":future, "Owenr":Owenr}
        data = collection.insert_one(newmember)
        return data

    def allmembers(collection, Owenr):
        collection = db[collection]
        mem = {"Owenr":Owenr}
        members = collection.find(mem)
        countmembers = collection.count_documents(mem)
        return members, countmembers

    def editmembers(collection, fullname, membership, endmembership, Owenr):
        collection = db[collection]
        member = {"fullname":fullname, "Owenr":Owenr}
        new = {"$set":{"endmembership":endmembership, "membership":membership}}
        collection.update_one(member, new)

    def editmembers1(collection, fullname, spot, future, Owenr):
        collection = db[collection]
        member = {"fullname":fullname, "Owenr":Owenr}
        new = {"$set":{"spot":spot, "future":future}}
        collection.update_one(member, new)

    def deletemembers(collection, fullname, Owenr):
        collection = db[collection]
        member = {"fullname":fullname, "Owenr":Owenr}
        collection.delete_one(member)