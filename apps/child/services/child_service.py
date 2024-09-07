from apps.child.models import Child
from apps.parents.models import Parent

def create_child_for_parent(parent_id, child_data, avatar=None):
    try:
        parent = Parent.objects.get(id=parent_id)
        allowed_fields = ['name', 'last_name', 'birth_date', 'autism_level', 'avatar']
        filtered_data = {key: value for key, value in child_data.items() if key in allowed_fields}
        if avatar:
            filtered_data['avatar'] = avatar
        child = Child.objects.create(parent=parent, **filtered_data)
        return child
    except Parent.DoesNotExist:
        return None

def get_children_by_parent(parent_id):
    try:
        parent = Parent.objects.get(id=parent_id)
        return Child.objects.filter(parent=parent)
    except Parent.DoesNotExist:
        return None

def get_child_by_parent(parent_id, child_id,avatar=None):
    try:
        parent = Parent.objects.get(id=parent_id)
        return Child.objects.get(parent=parent, id=child_id)
    except (Parent.DoesNotExist, Child.DoesNotExist):
        return None

def update_child_for_parent(parent_id, child_id, data, avatar=None):
    try:
        parent = Parent.objects.get(id=parent_id)
        child = Child.objects.get(parent=parent, id=child_id)
        allowed_fields = ['name', 'last_name', 'birth_date', 'autism_level', 'avatar']
        for key, value in data.items():
            if key in allowed_fields:
                setattr(child, key, value)
        if avatar:
            child.avatar = avatar
        child.save()
        return child
    except (Parent.DoesNotExist, Child.DoesNotExist):
        return None

def delete_child_for_parent(parent_id, child_id):
    try:
        parent = Parent.objects.get(id=parent_id)
        child = Child.objects.get(parent=parent, id=child_id)
        child.delete()
        return True
    except (Parent.DoesNotExist, Child.DoesNotExist):
        return False

def count_children(parent_id):
    try:
        parent = Parent.objects.get(id=parent_id)
        return Child.objects.filter(parent=parent).count()
    except Parent.DoesNotExist:
        return 0