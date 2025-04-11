def get_unique_or_none(model, **kwargs):
    """
    Gets instance or none for provided Model.

    Args:
        model: Requested Model
    
    Returns:
        Single instance of the requested model or None
    """
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    except model.MultipleObjectsReturned:
        return None