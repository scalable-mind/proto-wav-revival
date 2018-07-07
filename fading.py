seconds = float
Hz = int
samples = Hz

def seconds_to_samples(sample_rate: Hz, length: seconds):
    return int(length * sample_rate)


def fade_in(samples: samples):
    for i in range(samples):
        yield i/samples

def fade_out(samples: samples):
    for i in range(samples):
        yield -i/samples + 1 - 1/samples


# def fade_in(length: samples):
#     pass


# def fade_out(sample_rate: Hz, length: seconds):
#     pass


def fade(zeros: int, sample_rate: Hz, in_length: seconds, out_length: seconds):
    pass


def fade_cross(length_in: samples, length_out: samples, zeros: samples):
    if length_in + length_out <= zeros :
        return -1
    else:


if __name__ == '__main__':
    samples_in = seconds_to_samples(48000, 0.1)
    samples_out = seconds_to_samples(48000, 0.2)
    print(list(fade_in(samples_in)))
    print(list(fade_out(samples_out)))
