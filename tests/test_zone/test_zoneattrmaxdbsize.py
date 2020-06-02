import unittest

from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from tests.test_zone.zone_vars import *

log = logging.getLogger(__name__)

class TestZoneAttrMaxdbSize(unittest.TestCase):

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

    def test_maxdb_size_read(self):
        self.z.create()
        log.debug("Max DB Size : " + str(self.z.maxdb_size))

    def test_maxdb_size_read_nonexisting(self):
        log.debug("Max DB Size(nonexisting) : " + str(self.z.maxdb_size))

    def test_maxdb_size_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.z.maxdb_size = "asdf"
        self.assertEqual('can\'t set attribute',str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()