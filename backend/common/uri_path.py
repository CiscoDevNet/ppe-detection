# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------


class UriPath:
    def __init__(self, uri):
        self.params = {}
        index = uri.find("?")
        if index != -1:
            self.base = uri[0:index]
            line = uri[index + 1:]
            if len(line) != 0:
                for part in line.split("&"):
                    li = part.find("=")
                    key = part
                    value = ""
                    if li != -1:
                        key = part[0: li]
                        value = part[li + 1:]

                    values = self.params[key]
                    if values is None:
                        values = []
                        self.params[key] = values
                    values.append(value)
        else:
            self.base = uri
        self.base = self.strip(self.base, '/')

    @staticmethod
    def strip(s, strip_chars):
        if s.startswith(strip_chars):
            s = s[len(strip_chars):]
        if s.endswith(strip_chars):
            s = s[0:len(s) - len(strip_chars)]
        return s

