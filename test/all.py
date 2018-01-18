import chunk_codec
import client
import codec_login_logout
import codec_play
import command
import doctestsuite
import geometry
import protocol_login_logout
import protocol_play
import protocol_unconnected
import world


# noinspection PyUnusedLocal
def load_tests(loader, tests, pattern):
    modules = (
        doctestsuite,
        geometry,
        command,
        chunk_codec,
        codec_login_logout,
        codec_play,
        protocol_unconnected,
        protocol_login_logout,
        protocol_play,
        world,
        client,
    )
    suite = unittest.TestSuite()
    for m in modules:
        suite.addTests(loader.loadTestsFromModule(m))
    return suite


if __name__ == '__main__':
    import unittest
    unittest.main()
