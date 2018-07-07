from enum import Enum, unique
import numpy as np


@unique
class SampleState(Enum):
    ZERO_STATE = 0
    ONE_STATE = 1


def gen_smooth(samples_compressed: list, silence_samples_len: int) -> list:
    if len(samples_compressed) < 2:
        raise Exception('Wrong `samples_compressed` length: {length}.'.format(length=len(samples_compressed)))

    samples_data = samples_compressed[1:]
    if 0 in samples_data:
        raise Exception('`samples_data` must not contain zeroes.')
    if len(samples_data) == 1:
        yield samples_compressed[0]
        yield samples_data[0]
        return

    if _start_with_silence(samples_compressed):
        yield 0     # also starts with silence
        yield samples_data[0]   # copy the first silence sample
        del samples_data[0]
    else:
        yield 1     # result starts with 1

    sample_smoothed = 0
    state = SampleState.ONE_STATE
    for sample in samples_data:     # where len(samples_data) > 1

        if state == SampleState.ZERO_STATE:
            if sample <= silence_samples_len:
                sample_smoothed += sample
            else:
                yield sample_smoothed
                yield sample
                sample_smoothed = 0
            state = SampleState.ONE_STATE

        elif state == SampleState.ONE_STATE:
            sample_smoothed += sample
            state = SampleState.ZERO_STATE

        else:
            raise Exception('Unrecognized state: {state}'.format(state=state))

    if sample_smoothed != 0:
        yield sample_smoothed


def smooth(samples_compressed: list, silence_samples_len: int) -> list:
    if len(samples_compressed) < 2:
        raise Exception('Wrong `samples_compressed` length: {length}.'.format(length=len(samples_compressed)))

    samples_data = samples_compressed[1:]
    if 0 in samples_data:
        raise Exception('`samples_data` must not contain zeroes.')
    if len(samples_data) == 1:
        return list(samples_compressed)  # copy

    result = []

    if _start_with_silence(samples_compressed):
        result.append(0)  # also starts with silence
        result.append(samples_data[0])  # copy the first silence sample
        del samples_data[0]
    else:
        result.append(1)  # result starts with 1

    sample_smoothed = 0
    state = SampleState.ONE_STATE
    for sample in samples_data:  # where len(samples_data) > 1

        if state == SampleState.ZERO_STATE:
            if sample <= silence_samples_len:
                sample_smoothed += sample
            else:
                result.append(sample_smoothed)
                result.append(sample)
                sample_smoothed = 0
            state = SampleState.ONE_STATE

        elif state == SampleState.ONE_STATE:
            sample_smoothed += sample
            state = SampleState.ZERO_STATE

        else:
            raise Exception('Unrecognized state: {state}'.format(state=state))

    # If the last sample did contain ones or
    # zeroes less than `silence_samples_len`,
    # then the last `sample_smoothed` value
    # is not in `result` yet, but it is not 0,
    # so we should add it manually after the loop:
    if sample_smoothed != 0:
        result.append(sample_smoothed)

    return result

def _start_with_silence(samples_compressed: list) -> bool:
    return samples_compressed[0] == 0


def _test_smooth(*args, expected):
    actual = smooth(args[0], args[1])
    assert actual == expected, 'actual != expected; actual == {a}; expected == {e}'.format(a=actual, e=expected)


def _test_gen_smooth(*args, expected):
    actual = list(gen_smooth(args[0], args[1]))
    assert actual == expected, 'actual != expected; actual == {a}; expected == {e}'.format(a=actual, e=expected)


if __name__ == '__main__':
    for i, j, k in [
        ([0, 4], 5, [0, 4]),
        ([0, 4, 5], 5, [1, 9]),
        ([0, 4, 5], 3, [0, 4, 5]),
        ([0, 4, 5, 3], 5, [1, 12]),
        ([0, 4, 5, 3], 3, [0, 4, 8]),
        ([0, 4, 5, 3], 2, [0, 4, 5, 3]),
        ([0, 4, 5, 4], 3, [0, 4, 5, 4]),
        ([1, 4], 5, [1, 4]),
        ([1, 4, 5], 4, [1, 4, 5]),
        ([1, 4, 5], 5, [1, 9]),
        ([1, 4, 5, 4, 6, 4, 5, 4, 6], 5, [1, 13, 6, 13, 6])
    ]:
        _test_smooth(i, j, expected=k)
        _test_gen_smooth(i, j, expected=k)
