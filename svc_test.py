import pytest
from svc import LogService, DuplicateKey, NotFound, InvalidLog

def test_getLog():
    s = LogService()
    cases = {
        "foo": "bar",
        "footwo": "bartwo",
        "foothree": "foothree"
    }

    for k, v in cases.items():
        s.records[k] = v
        assert s.getLog(k) == v


def test_putLog():
    s = LogService()
    cases = {
        "u_123" : {
            "type": "user",
            "timestamp": "2024-03-01T13:45:00.000Z",
            "event_id": "u_123",
            "event": {
                "username": "my_user",
                "email": "my_user@email.com",
                "operation": "read/write"
            }
        },
        "s_123" : {
            "type": "system",
            "timestamp": "2024-02-01T13:45:00.000Z",
            "event_id": "s_123",
            "event": {
                "system_id": "id_123",
                "location": "europe",
                "operation": "read/write"
            }
        }

    }

    for k, v in cases.items():
        s.putLog(v)
        assert s.records[k] == v


def test_putLogRaisesDuplicateKey():
    s = LogService()
    s.putLog(
        {
            "type": "system",
            "timestamp": "2024-02-01T13:45:00.000Z",
            "event_id": "s_123",
            "event": {
                "system_id": "id_123",
                "location": "europe",
                "operation": "read/write"
            }
        }
    )

    with pytest.raises(DuplicateKey):
        s.putLog(
            {
                "type": "system",
                "timestamp": "2024-02-01T13:45:00.000Z",
                "event_id": "s_123",
                "event": {
                    "system_id": "id_123",
                    "location": "europe",
                    "operation": "read/write"
                }
            }

        )

def test_dateTimeValidation():
    s = LogService()
    cases = {
        "2024-03-01T13:45:00.000Z" : True,
        "2024-01-01T13:45:00.000Z" : True,
        "2025-03-01T13:45:00.000Z" : False,
        "2025-03-01T13:45:00.000Z" : False,
    }

    for t, expect in cases.items():
        actual = s.validDateTime(t)
        assert actual == expect, f"case: {t}, expecting: {expect}, got: {actual}"

def test_putLogCatchesInvalidLogs():
    s = LogService()
    cases = [
        {
            "type": "foo",
            "timestamp": "2024-02-01T13:45:00.000Z",
            "event_id": "s_123",
            "event": {
                "system_id": "id_123",
                "location": "europe",
                "operation": "read/write"
            }
        },
        {
            "type": "system",
            "timestamp": "2024-02-01T13:45:00.000Z",
            "event_id": "s_123",
            "event": {
                "system_id": "id_123",
                "location": "mexico",
                "operation": "read/write"
            }
        },
        {
            "type": "system",
            "timestamp": "2026-02-01T13:45:00.000Z",
            "event_id": "s_123",
            "event": {
                "system_id": "id_123",
                "location": "europe",
                "operation": "read/write"
            }
        }
    ]

    for log in cases:
        with pytest.raises(InvalidLog):
            s.putLog(log)
