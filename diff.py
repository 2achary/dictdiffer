class Diff():
    """
    Show the difference between two given dicts 'old' and 'new'.

    Intended to be used in an auditing system that checks existing
    records in a nosql database ('old') and compares them with a
    request to update the record ('new') and store the difference
    in a separate database.

    See test_diff.py for expected output for each method.

    Will need recursive methods for nested dicts

    Use dot notation for the path to the key that is different e.g. {"a.b.c": "modified value"}

    Must not convert dicts to sets. Because of the billions of records that will be compared,
    conversion to sets, then back to dicts would drastically slow down the process.
    """

    def __init__(self):
        self.depth = []
        self.results = []

    def added(self, old, new):
        for key in new:
            if key not in old:
                if self.depth:
                    self.results.append({
                        'operation': 'ADDED',
                        'field': '.'.join(self.depth) + '.' + str(key),
                        'new': new[key]
                    })
                else:
                    self.results.append({
                        'operation': 'ADDED',
                        'field': str(key),
                        'new': new[key]
                    })
            else:
                if type(old[key]) == dict and type(new[key]) == dict:
                    self.depth.append(str(key))
                    self.added(old[key], new[key])

        if self.depth:
            self.depth.pop()
        else:
            return self.results

    def modified(self, old, new):
        for key in [key for key in new if key in old]:
            if type(old[key]) == dict and type(new[key]) == dict:
                self.depth.append(str(key))
                self.modified(old[key], new[key])

            elif old[key] != new[key]:
                if self.depth:
                    self.results.append({
                        'operation': 'MODIFIED',
                        'field': '.'.join(self.depth) + '.' + str(key),
                        'old': old[key],
                        'new': new[key]
                    })
                else:
                    self.results.append({
                        'operation': 'MODIFIED',
                        'field': str(key),
                        'old': old[key],
                        'new': new[key]
                    })

        if self.depth:
            self.depth.pop()
        else:
            return self.results

    def deleted(self, old, new):
        for key in old:
            if key not in new:
                if self.depth:
                    self.results.append({
                        'operation': 'DELETED',
                        'field': '.'.join(self.depth) + '.' + str(key),
                        'old': old[key]
                    })
                else:
                    self.results.append({
                        'operation': 'DELETED',
                        'field': str(key),
                        'old': old[key]
                    })
            else:
                if type(old[key]) == dict and type(new[key]) == dict:
                    self.depth.append(str(key))
                    self.deleted(old[key], new[key])

        if self.depth:
            self.depth.pop()
        else:
            return self.results

    def combine_results(self, old, new):
        self.added(old, new)
        self.modified(old, new)
        self.deleted(old, new)
        return self.results

    def difference(self, old, new):
        d = {}
        d['difference'] = self.combine_results(old, new)
        return d
