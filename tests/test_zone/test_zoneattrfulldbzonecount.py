import unittest

from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from tests.test_zone.zone_vars import *

log = logging.getLogger(__name__)

class TestZoneAttrFulldbZoneCount(unittest.TestCase):

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
        self.z = Zone(self.switch, self.id, "test_zone")

    def test_fulldb_zone_count_read(self):
        self.z.create()
        log.debug("Full DB Zone Count : " + str(self.z.fulldb_zone_count))
        self.assertIsNotNone(self.z.fulldb_zone_count)

    def test_fulldb_zone_count_read_nonexisting(self):
        log.debug("Full DB Zone Count(nonexisting) : " + str(self.z.fulldb_zone_count))
        self.assertIsNotNone(self.z.fulldb_zone_count)

    def test_fulldb_zone_count_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.z.fulldb_zone_count = "asdf"
        self.assertEqual('can\'t set attribute',str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()