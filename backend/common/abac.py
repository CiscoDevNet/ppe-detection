# ----------------------------------------------------------------
# Copyright 2018 Cisco Systems
#
# Author: coliu@cisco.com
# -----------------------------------------------------------------


from common import ContinueI

EmptyPermissions = [{}]
AnonymousPermissions = [{"user": "__anonymous__"}]
SudoPermissions = [{"user": "*", "company": "*", "role": "*", "domain": "*"}]

AccessRead = 1
AccessWrite = 2
AccessDelete = 4


def can_access_rest(user_perms, abac, http_verb):
    op = {
        "GET": 'read',
        "POST": 'write',
        "PUT": 'write',
        "PATCH": 'write',
        "DELETE": 'delete'
    }.get(http_verb, 'read')
    return can_access(user_perms, abac.get(op, []))


def can_access(subject_perms, target_perms):
    if not subject_perms or len(subject_perms) == 0:
        subject_perms = AnonymousPermissions

    if not target_perms or len(target_perms) == 0:
        target_perms = EmptyPermissions

    # If the subject has no permissions, or the target has no permissions,
    # or the target has an empty PermList we do the safe thing and deny access.
    for subject in subject_perms:
        for target in target_perms:
            try:
                if len(target) == 0:
                    # target PermList is empty, ignore it rather than treat it as full access.
                    # However, if subject permissions are ALL wildcard, then make an exception
                    for k, v in subject.items():
                        if "*" != v:
                            raise ContinueI()
                    return True  # subject is all wildcards, allow access
                for key, target_val in target.items():
                    if target_val != "":
                        if "*" == target_val:
                            continue  # target accepts any value for the attribute
                        subject_val = subject.get(key)
                        if subject_val and (subject_val == target_val or "*" == subject_val):
                            # Subject value matches or it's a wildcard
                            continue
                    raise ContinueI()  # this doesn't match, try the next one
                return True  # subject fully matches target, we can access this
            except ContinueI:
                continue
    return False


class PermissionedObject:
    def __init__(self, perms):
        self.perms = perms

    def is_readable_by(self, abac):
        return can_access(self.perms, abac.read)

    def is_writeable_by(self, abac):
        return can_access(self.perms, abac.write)

    def is_deleteable_by(self, abac):
        return can_access(self.perms, abac.delete)

    def is_accessible_by(self, abac, access):
        return ((access&AccessRead) == 0 or can_access(self.perms, abac.read)) and ((access&AccessWrite) == 0 or can_access(self.perms, abac.write)) and ((access&AccessDelete) == 0 or can_access(self.perms, abac.delete))

    def filter_objects(self, objs, access):
        if isinstance(objs, list):
            ret = []
            for obj in objs:
                if self.is_accessible_by(obj, access):
                    ret.append(obj)
            return ret;
        elif isinstance(objs, dict):
            ret = {};
            for key, value in objs.items():
                if self.is_accessible_by(value, access):
                    ret[key] = value
            return ret
        else:
            raise Exception("Expected an array or object")

    def filter_readable_objects(self, objs):
        return self.filter_objects(objs, AccessRead)

    def filter_writeable_objects(self, objs):
        return self.filter_objects(objs, AccessWrite)

    def filter_deleteable_objects(self, objs):
        return self.filter_objects(objs, AccessDelete)


class ABAC:
    def __init__(self, _read, _write, _delete):
        self.read = _read
        self.write = _write
        self.delete = _delete


MemberAbac = ABAC([{'role': 'member'}], [{'role': 'member'}], [{'role': 'member'}])
