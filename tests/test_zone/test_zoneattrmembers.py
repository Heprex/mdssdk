import unittest

from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from tests.test_zone.zone_vars import *
from mdssdk.fc import Fc
from mdssdk.portchannel import PortChannel
from mdssdk.devicealias import DeviceAlias

log = logging.getLogger(__name__)

class TestZoneAttrMembers(unittest.TestCase):

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

    def test_members_read(self):
        fc_name = ""
        for k,v in list(self.switch.interfaces.items()):
            if type(v) is Fc:
                fc_name = k
                break
        while True:
            pc_id = get_random_id(1, 256)
            if "port-channel"+str(pc_id) not in self.switch.interfaces.keys():
                break
        pc = PortChannel(self.switch, pc_id)
        d = DeviceAlias(self.switch)
        olddb = d.database
        if olddb is None:
            da_name = get_random_string()
            da_pwwn = get_random_pwwn()
        else:
            while True:
                da_name = get_random_string()
                da_pwwn = get_random_pwwn()
                if da_name not in olddb.keys() and da_pwwn not in olddb.values():
                    break
        d.create({da_name: da_pwwn})
        members = [{'pwwn': '50:08:01:60:08:9f:4d:00'},
                    {'interface': fc_name},
                    {'device-alias': da_name},
                    {'ip-address': '1.1.1.1'},
                    {'symbolic-nodename': 'symbnodename'},
                    {'fwwn': '11:12:13:14:15:16:17:18'},
                    {'fcid': '0x123456'},
                    {'interface': pc.name},
                    {'fcalias': 'somefcalias'}]
        self.switch.config('fcalias name somefcalias vsan ' + str(self.id))
        self.z.add_members(members)
        mem = self.z.members
        d.delete(da_name)
        log.debug("Given Zone Members : " + str(members))
        log.debug("Zone Members : " + str(mem))
        self.assertEqual(len(members), len(mem))

    def test_members_read_nonexisting(self):
        self.assertIsNone(self.z.members)

    def test_members_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.z.members = []
        self.assertEqual('can\'t set attribute', str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()