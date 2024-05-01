from datetime import datetime

class NotFound(Exception):
    def __init__(self, message):
        super().__init__(message)

class DuplicateKey(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidLog(Exception):
    def __init__(self, message):
        super().__init__(message)


class LogService:
    def __init__(self):
        self.records = {}
        self.recordLimit = 1000
        self.dateTimeFormat = "%Y-%m-%dT%H:%M:%S.%fZ"

    def getLog(self, eventID):
        try:
            log = self.records[eventID]
        except KeyError:
            raise NotFound("not_found")
        return log

    def putLog(self, log):
        if len(self.records.keys()) >= self.recordLimit:
            raise RecordLimit("record_limit")
        eventID = log["event_id"]
        try:
            found = self.records[eventID]
            if found is not None:
                raise DuplicateKey("event_id_exists")
        except KeyError:
            try:
                if self.validLog(log):
                    self.records[eventID] = log
            except InvalidLog as e:
                raise e



    def validDateTime(self, dt):
       t = datetime.strptime(dt, self.dateTimeFormat)
       return t < datetime.now()

    def validSystemLog(self, sysLog):
        if not self.validDateTime(sysLog["timestamp"]):
            raise InvalidLog("inavlid_timestamp")

        validLocs = ["us", "europe"]
        if sysLog["event"]["location"] not in validLocs:
            raise InvalidLog("invalid_location")

        return True


    def validUserLog(self, usrLog):
        if not self.validDateTime(usrLog["timestamp"]):
            raise InvalidLog("inavlid_datetime")

        return True

    def validLog(self, log):
        match log["type"]:
            case "user":
                return self.validUserLog(log)
            case "system":
                return self.validSystemLog(log)
            case _:
                raise InvalidLog("invalid_log_type")
