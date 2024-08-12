# Flow Log Data Processor

## Overview

The Flow Log Processor is a Python-based tool that processes flow log data by mapping each log entry to a specific tag based on a lookup table. The tool reads flow logs in a specific format, matches the entries with tags provided in a CSV lookup table, and outputs a summary of the tag counts and the counts of port/protocol combinations.

## Assumptions

1. The flow log data file follows the format:

   ``` <version> <account-id> <interface-id> <srcaddr> <dstaddr> <srcport> <dstport> <protocol> <packets> <bytes> <start> <end> <action> <log-status> ```
2. The flow log data is in the version 2 default format, which includes 14 fields:
    ##### VERSION_2_FIELDS_COUNT = 14
    ##### DSTPORT_FIELD_INDEX = 6 (destination port)
    ##### PROTOCOL_FIELD_INDEX = 7 (protocol)

3. The flow log file is in plain text format with the `.txt` extension.
4. The lookup table is a CSV file with 3 columns: `dstport`, `protocol`, and `tag`.
5. The `dstport` and `protocol` values in the flow log file are case-insensitive.
6. The lookup table may contain same tags for different `dstport` and `protocol` combinations, but the mapping for each combination is unique.
7. The tool expects the output file to have a `.txt` extension.

## Requirements

- Python 3.x

## Protocol Number Mapping

The tool uses a protocol number mapping based on the IANA Protocol Numbers. This mapping allows the tool to interpret the protocol numbers in the flow logs and match them against the protocol names specified in the lookup table.


## Usage

### Command-line Arguments

- `--lookup-file` or `-l`: Path to the lookup table CSV file.
- `--input-file` or `-i`: Path to the flow log TXT file.
- `--output-file` or `-o`: Path to the output TXT file. Must have a `.txt` extension.

### Example Command

```bash
python main.py --lookup-file lookup_table.csv --input-file flow_logs.txt --output-file output.txt
```

## Testing

The project includes a set of unit tests to verify the functionality. These tests can be executed using the unittest framework. To run the tests, use the following command:

```bash
python -m unittest discover -s tests
```
This command will discover and run all test cases in the tests directory.

### Test Cases
The test cases cover various aspects of the tool, including:

1. File Existence Validation: Ensures that the input files exist before processing.
2. File Format Validation: Verifies that the input files are in the correct format (e.g., .csv for lookup tables and .txt for flow logs).
3. Lookup Table Parsing: Tests the correct parsing of the lookup table CSV file into the expected format.
4. Flow Log Processing: Ensures that flow logs are processed correctly, matching entries to tags based on the lookup table.
5. Output Generation: Validates that the output file is generated correctly with the expected content.

## Project Structure

- main.py: The entry point for the application, responsible for handling command-line arguments and performing the flow log processing.
- solution.py: Contains the core logic for reading the lookup table, processing flow logs, and generating the output file.
- protocol_number_mapping.py: Handles the mapping between protocol numbers and their corresponding names, based on the IANA Protocol Numbers.
- logger.py: Implements logging functionality to track the processing steps and any issues encountered.
- constant.py: Defines constants used throughout the project.
- test.py: Contains unit tests for validating the functionality of the tool.

## References
[IANA Protocol Numbers](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml) 

[Flow Log Record Examples](https://docs.ionos.com/cloud/network-services/flow-logs/record-example)

[AWS VPC Flow Log Records](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html)
