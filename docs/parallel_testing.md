# Parallel Test Execution Framework

This document explains how to use the parallel test execution framework in the Selenium Connecteam project.

## Overview

The parallel test execution framework allows you to run tests in parallel, which can significantly reduce the test execution time. The framework uses the pytest-xdist plugin, which provides test distribution and parallel execution capabilities.

## Prerequisites

- pytest-xdist package (included in requirements.txt)
- Multiple processor cores (for actual parallelism)

## Test Distribution Modes

The framework supports different test distribution modes:

1. **loadscope** - Tests in the same scope (e.g., class) will be run in the same worker. This preserves test dependencies within a class.
2. **each** - Each test is run in a separate worker, maximizing parallelism but potentially ignoring dependencies.
3. **loadfile** - Tests in the same file will be run in the same worker.
4. **loadgroup** - Tests in the same group (defined by markers) will be run in the same worker.

## Running Parallel Tests

### Using Command Line

To run tests in parallel from the command line:

```bash
# Run with auto-detected number of workers
python -m pytest -n auto tests/

# Run with specific number of workers
python -m pytest -n 4 tests/

# Run with specific distribution mode
python -m pytest -n 4 --dist=loadscope tests/
```

### Using Provided Scripts

We've provided scripts in the `scripts/` directory to simplify running parallel tests:

1. **Basic parallel test execution:**
   ```bash
   python3 scripts/run_parallel_tests.py [num_workers]
   ```

2. **Running apply CV tests in parallel:**
   ```bash
   python3 scripts/run_parallel_apply_cv.py [num_workers]
   ```

3. **Running parameterized tests in parallel:**
   ```bash
   python3 scripts/run_parallel_parameterized.py [num_workers]
   ```

If `num_workers` is not specified, a default value will be used.

## IDE Compatibility

When using an IDE like PyCharm to run individual tests, the parallel execution options should be disabled to avoid conflicts. For this reason, our `pytest.ini` file includes only basic configuration options.

When running individual tests from PyCharm:
- Right-click on a test function or class and select "Run" or "Debug" 
- PyCharm will run the test without parallel execution options

When running tests in parallel:
- Use the command line or the provided scripts
- Manually specify the `-n` and `--dist` options

### Common Issues with IDE Test Runners

If you see errors like:
```
ERROR: unrecognized arguments: --dist=loadscope -n test_file.py::TestClass::test_method
```

This indicates that the parallel execution options are conflicting with the specific test you're trying to run. Make sure to:

1. Run specific tests without parallel options
2. Run parallel tests using the command line or provided scripts
3. Keep the `addopts` setting in `pytest.ini` free of parallel execution options


In `each` mode, each parameter combination will run in a separate worker.

## Best Practices

1. **Resource Isolation**: Ensure tests don't share resources that could cause conflicts.
2. **Test Independence**: Design tests to be independent of each other.
3. **Fixture Scoping**: Use function-scoped fixtures to ensure clean test environments.
4. **Worker Count**: Use a number of workers that matches your system's capabilities (typically # of cores - 1).
5. **Distribution Mode**: Choose the distribution mode that best suits your test dependencies.

## Performance Considerations

- Parallel execution requires more system resources (CPU, memory).
- WebDriver instances require significant resources, so monitor system performance.
- Too many parallel workers might degrade performance due to resource contention.

## Troubleshooting

1. **Tests Failing in Parallel but Passing Sequentially**: This often indicates resource conflicts or test interdependencies.
2. **Poor Performance**: Reduce the number of workers or check for resource bottlenecks.
3. **WebDriver Issues**: Ensure each worker can start its own browser instance without conflicts.

## Further Reading

- [pytest-xdist Documentation](https://pytest-xdist.readthedocs.io/en/latest/)
- [Selenium WebDriver Documentation](https://www.selenium.dev/documentation/webdriver/) 