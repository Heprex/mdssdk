import unittest

from mdssdk.zoneset import ZoneSet
from mdssdk.zone import Zone
from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError
from tests.test_zoneset.zoneset_vars import *

log = logging.getLogger(__name__)

class TestZoneSetAttrMembers(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        self.vsandb = sw.vsans
        while True:
            self.id = get_random_id()
            if self.id not in self.vsandb.keys():
                break
        self.v = Vsan(switch=self.switch, id=self.id)
        self.v.create()
        self.zoneset = ZoneSet(self.switch, self.id, "test_zoneset")
        self.zoneset.create()

    def test_members_read(self):
        self.skipTest("needs to be fixed")
        zone1 = Zone(self.switch, self.id, "test_zone1")
        zone1.create()
        zone2 = Zone(self.switch, self.id, "test_zone2")
        zone2.create()
        members = [zone1, zone2]
        self.zoneset.add_members(members)
        self.assertEqual([zone.name for zone in members], list(self.zoneset.members.keys()))

    def test_members_read_nonexisting(self):
        self.assertIsNone(self.zoneset.members)

    def test_members_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.zoneset.members = "asdf"
        self.assertEqual('can\'t set attribute', str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()