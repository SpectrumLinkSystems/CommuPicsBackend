from apps.child.models import Child
from apps.child.models.collection import Collection

class CollectionService:
    def __init__(self):
        pass

    @staticmethod
    def create_many_collections(self, collections):
        new_ids = []
        for collection in collections:
            new_collection = Collection.objects.create(
                name=collection['name'],
                image_url=collection['image_url'],
                child_id=Child(id=collection['child_id']),
            )
            new_ids.append(new_collection.id)
        return new_ids
