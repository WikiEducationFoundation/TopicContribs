import logging


class RevHistory(object):

    def __init__(self, page):
        self._revisions = []
        recent_sha1 = []
        recent = []
        for rev in page:
            if rev.sha1 in recent_sha1:
                cut_off = recent_sha1.index(rev.sha1) + 1
                recent_sha1 = recent_sha1[:cut_off]
                recent = recent[:cut_off]
                continue
            recent_sha1.append(rev.sha1)
            recent.append(rev)
            if len(recent) > 10:
                recent_sha1.pop(0)
                self._revisions.append(recent.pop(0))
        self._revisions.extend(recent)

    def revert_free_revisions(self):
        return self._revisions
