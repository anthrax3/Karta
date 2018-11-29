from lib_template import *
import string

class OpenSSLSeeker(Seeker):
    # Library Name
    NAME = 'OpenSSL'
    # version string marker
    VERSION_STRING = " part of OpenSSL "

    # Overriden base function
    def searchLib(self, logger):
        key_string = self.VERSION_STRING
        ids = ['SHA1', 'SHA-256', 'SHA-512', 'SSLv3', 'TLSv1', 'ASN.1', 'EVP', 'RAND', 'RSA', 'Big Number']

        # Now search
        self._version_strings = []
        seen_copyrights = set()
        match_counter = 0
        for bin_str in self._all_strings:
            # we have a match
            if key_string in str(bin_str):
                copyright_string = str(bin_str)
                # check for a supporting key word id
                if len(filter(lambda id : id in copyright_string, ids)) == 0:
                    # false match
                    continue
                # check for a duplicate inside the same library
                chopped_copyright_string = copyright_string[copyright_string.find(key_string) : ]
                if match_counter >= 1 and chopped_copyright_string in seen_copyrights :
                    continue
                # valid match
                logger.debug("Located a copyright string of %s in address 0x%x", self.NAME, bin_str.ea)
                match_counter += 1
                seen_copyrights.add(chopped_copyright_string)
                # save the string for later
                self._version_strings.append(chopped_copyright_string)

        # return the result
        return len(self._version_strings)

    # Overriden base function
    def identifyVersions(self, logger):
        results = []
        # extract the version from the copyright string
        for work_str in self._version_strings:
            results.append(self.extractVersion(work_str, start_index = work_str.find(self.NAME) + len(self.NAME) + 1, legal_chars = string.digits + string.ascii_lowercase + '.'))
        # return the result
        return results

# Register our class
OpenSSLSeeker.register(OpenSSLSeeker.NAME, OpenSSLSeeker)
