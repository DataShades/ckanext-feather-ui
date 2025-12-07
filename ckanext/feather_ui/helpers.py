import ckan.model as model


def fui_get_organisation_object(org_id: str) -> model.Group | None:
    return model.Group.get(org_id)
