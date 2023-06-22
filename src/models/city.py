from tortoise import fields
from tortoise.models import Model


class City(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(100)
    state = fields.CharField(100, null=True)
    lat = fields.DecimalField(max_digits=9, decimal_places=6)
    long = fields.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        table = "cities"

    def to_dict(self):
        return {
            "name": self.name,
            "lat": self.lat,
            "long": self.long,
        }
