from bson import ObjectId


def to_object_id(value: str) -> ObjectId:
    """
    Convert string into MongoDB ObjectId.
    """

    if not ObjectId.is_valid(value):
        raise ValueError("Invalid ObjectId")

    return ObjectId(value)