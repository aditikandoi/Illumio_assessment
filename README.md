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
4. The lookup table is a CSV file with columns: `dstport`, `protocol`, and `tag`.
5. The `dstport` and `protocol` values in the flow log file are case-insensitive.
6. The lookup table may contain multiple tags for different `dstport` and `protocol` combinations, but the mapping for each combination is unique.
7. The tool expects the output file to have a `.txt` extension.

## Requirements

- Python 3.x

## Usage

### Command-line Arguments

- `--lookup-file` or `-l`: Path to the lookup table CSV file.
- `--input-file` or `-i`: Path to the flow log TXT file.
- `--output-file` or `-o`: Path to the output TXT file. Must have a `.txt` extension.

### Example Command

```bash
python main.py --lookup-file lookup_table.csv --input-file flow_logs.txt --output-file output.txt
```

### References
[IANA Protocol Numbers](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml) 

[Flow Log Record Examples](https://docs.ionos.com/cloud/network-services/flow-logs/record-example)

[AWS VPC Flow Log Records](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html)
