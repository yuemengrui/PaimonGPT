# *_*coding:utf-8 *_*
# @Author : yuemengrui
import time
import random


class SnowFlake:

    def __init__(self, worker_id=0, sequence=0, worker_id_bits=7, sequence_bits=5, id_random=False):

        max_worker_id = -1 ^ (-1 << worker_id_bits)
        if id_random:
            worker_id = random.randint(1, max_worker_id)

        self.worker_id = worker_id
        self.sequence = sequence
        init_date = time.strptime('2024-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
        self.epoch_timestamp = int(time.mktime(init_date) * 1000000)
        self.last_timestamp = -1

        self.worker_id_shift = sequence_bits
        self.timestamp_left_shift = sequence_bits + worker_id_bits
        self.sequence_mask = -1 ^ (-1 << sequence_bits)

    def guid(self, to_str: bool = True):
        timestamp = self._current_timestamp()
        if timestamp < self.last_timestamp:
            raise 'clock is moving backwards. Rejecting requests until %s' % self.last_timestamp
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & self.sequence_mask
            if self.sequence == 0:
                timestamp = self._util_next_millis(self.last_timestamp)
        else:
            self.sequence = 0
        self.last_timestamp = timestamp
        nextid = ((timestamp - self.epoch_timestamp) << self.timestamp_left_shift) | (
                self.worker_id << self.worker_id_shift) | self.sequence
        if to_str:
            nextid = str(nextid)
        return nextid

    def _util_next_millis(self, last_timestamp):
        timestamp = self._current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._current_timestamp()
        return timestamp

    @staticmethod
    def _current_timestamp():
        return int(time.time() * 1000000)


snowflake = SnowFlake()
