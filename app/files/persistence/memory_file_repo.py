import uuid

class InMemoryFileRepo:
    def __init__(self):
        self.files = {}

    def list_by_owner(self, owner):
        return [f for f in self.files.values() if f["owner"] == owner]

    def create(self, owner, meta):
        fid = str(uuid.uuid4())
        self.files[fid] = {"id": fid, "owner": owner, **meta}
        return fid

    def get(self, owner, fid):
        f = self.files.get(fid)
        if not f or f["owner"] != owner:
            raise ValueError("Not found")
        return f

    def delete(self, owner, fid):
        self.files.pop(fid, None)

    def update(self, owner, fid, data):
        self.files[fid].update(data)
