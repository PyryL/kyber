from perf_tests.test_encryption import runner as encryption_test_runner
from perf_tests.test_ccakem import runner as ccakem_test_runner

encryption_test_runner()
ccakem_test_runner()
