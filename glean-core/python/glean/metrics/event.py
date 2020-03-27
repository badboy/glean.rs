# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import json
from typing import Dict, List, Optional


from .. import _ffi
from .._dispatcher import Dispatcher
from ..testing import ErrorType
from .. import _util


from .lifetime import Lifetime


class RecordedEventData:
    """
    Deserialized event data.
    """

    def __init__(
        self,
        category: str,
        name: str,
        timestamp: int,
        extra: Optional[Dict[str, str]] = None,
    ):
        """
        Args:
            category (str): The event's category, part of the full identifier.
            name (str): The event's name, part of the full identifier.
            timestamp (int): The event's timestamp, in milliseconds.
            extra (dict of str->str): Optional. Any extra data recorded for
                the event.
        """
        self._category = category
        self._name = name
        self._timestamp = timestamp
        if extra is None:
            extra = {}
        self._extra = extra

    @property
    def category(self):
        """The event's category, part of the full identifier."""
        return self._category

    @property
    def name(self):
        """The event's name, part of the full identifier."""
        return self._name

    @property
    def timestamp(self):
        """The event's timestamp."""
        return self._timestamp

    @property
    def extra(self):
        """Any extra data recorded for the event."""
        return self._extra

    @property
    def identifier(self):
        if self.category == "":
            return self.name
        else:
            return ".".join([self.category, self.name])


class EventMetricType:
    """
    This implements the developer facing API for recording events.

    Instances of this class type are automatically generated by
    `glean.load_metrics`, allowing developers to record values that were
    previously registered in the metrics.yaml file.

    The event API only exposes the `EventMetricType.record` method, which
    takes care of validating the input data and making sure that limits are
    enforced.
    """

    def __init__(
        self,
        disabled: bool,
        category: str,
        lifetime: Lifetime,
        name: str,
        send_in_pings: List[str],
        allowed_extra_keys: List[str],
    ):
        self._disabled = disabled
        self._send_in_pings = send_in_pings

        self._handle = _ffi.lib.glean_new_event_metric(
            _ffi.ffi_encode_string(category),
            _ffi.ffi_encode_string(name),
            _ffi.ffi_encode_vec_string(send_in_pings),
            len(send_in_pings),
            lifetime.value,
            disabled,
            _ffi.ffi_encode_vec_string(allowed_extra_keys),
            len(allowed_extra_keys),
        )

    def __del__(self):
        if getattr(self, "_handle", 0) != 0:
            _ffi.lib.glean_destroy_event_metric(self._handle)

    def record(self, extra: Optional[Dict[int, str]] = None):
        """
        Record an event by using the information provided by the instance of
        this class.

        Args:
            extra (dict of (int, str)): optional. This is a map from keys
                (which are enumerations) to values. This is used for events
                where additional richer context is needed. The maximum length
                for values is 100.
        """
        if self._disabled:
            return

        timestamp = _util.time_ms()

        @Dispatcher.launch
        def record():
            if extra is None:
                keys = []
                values = []
                nextra = 0
            else:
                keys, values = zip(*list(extra.items()))
                keys = [x.value for x in keys]
                nextra = len(extra)

            _ffi.lib.glean_event_record(
                self._handle,
                timestamp,
                _ffi.ffi_encode_vec_int32(keys),
                _ffi.ffi_encode_vec_string(values),
                nextra,
            )

    def test_has_value(self, ping_name: Optional[str] = None) -> bool:
        """
        Tests whether a value is stored for the metric for testing purposes
        only.

        Args:
            ping_name (str): (default: first value in send_in_pings) The name
                of the ping to retrieve the metric for.

        Returns:
            has_value (bool): True if the metric value exists.
        """
        if ping_name is None:
            ping_name = self._send_in_pings[0]

        return bool(
            _ffi.lib.glean_event_test_has_value(
                self._handle, _ffi.ffi_encode_string(ping_name)
            )
        )

    def test_get_value(
        self, ping_name: Optional[str] = None
    ) -> List[RecordedEventData]:
        """
        Returns the stored value for testing purposes only.

        Args:
            ping_name (str): (default: first value in send_in_pings) The name
                of the ping to retrieve the metric for.

        Returns:
            value (list of RecordedEventData): value of the stored events.
        """
        if ping_name is None:
            ping_name = self._send_in_pings[0]

        if not self.test_has_value(ping_name):
            raise ValueError("metric has no value")

        json_string = _ffi.ffi_decode_string(
            _ffi.lib.glean_event_test_get_value_as_json_string(
                self._handle, _ffi.ffi_encode_string(ping_name)
            )
        )

        json_content = json.loads(json_string)

        return [RecordedEventData(**x) for x in json_content]

    def test_get_num_recorded_errors(
        self, error_type: ErrorType, ping_name: Optional[str] = None
    ) -> int:
        """
        Returns the number of errors recorded for the given metric.

        Args:
            error_type (ErrorType): The type of error recorded.
            ping_name (str): (default: first value in send_in_pings) The name
                of the ping to retrieve the metric for.

        Returns:
            num_errors (int): The number of errors recorded for the metric for
                the given error type.
        """
        if ping_name is None:
            ping_name = self._send_in_pings[0]

        return _ffi.lib.glean_event_test_get_num_recorded_errors(
            self._handle, error_type.value, _ffi.ffi_encode_string(ping_name),
        )


__all__ = ["EventMetricType", "RecordedEventData"]
