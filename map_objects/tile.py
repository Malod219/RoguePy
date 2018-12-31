class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, blocked, block_sight=None, name=None):
        self.blocked = blocked

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
        self.explored = False
        self.name = name

    def to_json(self):
        json_data = {
            'blocked': self.blocked,
            'block_sight': self.block_sight,
            'explored': self.explored,
            'name': self.name
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        blocked = json_data.get('blocked')
        block_sight = json_data.get('block_sight')
        name = json_data.get('name')
        explored = json_data.get('explored')

        tile = Tile(blocked, block_sight, name)
        tile.explored = explored

        return tile
