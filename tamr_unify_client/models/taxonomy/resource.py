from tamr_unify_client.models.base_resource import BaseResource


class Taxonomy(BaseResource):
    """A project's taxonomy"""

    @classmethod
    def from_json(cls, client, data, api_path):
        return super().from_data(client, data, api_path)

    @property
    def name(self):
        """:type: str"""
        return self._data.get("name")

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"name={self.name!r})"
        )
