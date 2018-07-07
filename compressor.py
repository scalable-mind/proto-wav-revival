def compress(data):
    compressed = []
    compressed.append(data[0])
    current_value = compressed[0]
    curr_val_count = 1

    for sample in data[1:]:
        if sample == current_value:
            curr_val_count += 1
        else:
            compressed.append(curr_val_count)
            current_value = sample
            curr_val_count = 1
    compressed.append(curr_val_count)
    return compressed

def decompress(data):
    decompressed = []
    current_value = data[0]

    for sample in data[1:]:
        decompressed += [current_value] * sample
        current_value = 0 if current_value == 1 else 1

    return decompressed