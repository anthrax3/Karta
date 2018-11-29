from lib_template import *
import string

class MACTelnetSeeker(Seeker):
    # Library Name
    NAME = 'MAC-Telnet'
    # version string marker
    VERSION_STRING = "MAC-Telnet "
    DEAMON_STRING  = "MAC-Telnet Daemon "

    # Overriden base function
    def searchLib(self, logger):
        # Now search
        self._version_strings = []
        for bin_str in self._all_strings:
            # we have a match
            if self.VERSION_STRING in str(bin_str):
                version_string = str(bin_str)
                # check for the inner version string
                if self.DEAMON_STRING not in version_string:
                    # false match
                    continue
                # valid match
                logger.debug("Located a version string of %s in address 0x%x", self.NAME, bin_str.ea)
                # save the string for later
                self._version_strings.append(version_string)

        # return the result
        return len(self._version_strings)

    # Overriden base function
    def identifyVersions(self, logger):
        results = []
        # extract the version from the copyright string
        for work_str in self._version_strings:
            results.append(self.extractVersion(work_str, start_index = work_str.find(self.DEAMON_STRING) + len(self.DEAMON_STRING)))
        # return the result
        return results

# Register our class
MACTelnetSeeker.register(MACTelnetSeeker.NAME, MACTelnetSeeker)
