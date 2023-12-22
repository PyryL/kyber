from matplotlib import pyplot as plt
from random import randbytes
from os import path
from perf_tests.test_aes_integration import run as run_with_aes
from perf_tests.test_encryption import run as run_without_aes

test_sample_sizes = [32, 96, 192, 512, 1024, 1504, 2048, 4096, 8192, 10_048]

times_with_aes = []
times_without_aes = []

for i, payload_length in enumerate(test_sample_sizes):
    payload = randbytes(payload_length)

    durations = run_with_aes(payload)
    times_with_aes.append(sum(durations))

    durations = run_without_aes(payload)
    times_without_aes.append(sum(durations))

    print(f"{(i+1) / len(test_sample_sizes) * 100:.0f}% completed")

# save CSV
with open(path.join(path.dirname(__file__), "aes_comparison.csv"), "w") as file:
    file.write("payload size (bytes),time with AES,time without AES\n")
    for size, time_with_aes, time_without_aes in zip(test_sample_sizes, times_with_aes, times_without_aes):
        file.write(f"{size},{time_with_aes:.6f},{time_without_aes:.6f}\n")

# draw plot
plt.plot(test_sample_sizes, times_with_aes, marker="x", label="with AES")
plt.plot(test_sample_sizes, times_without_aes, marker="x", label="without AES")
plt.xlabel("Payload size, bytes")
plt.ylabel("Encryption + decryption time, seconds")
plt.legend(loc='upper left')
plt.show()
