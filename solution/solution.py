import os, csv
from collections import defaultdict
from common.constant import *
from common.logger import logger
from common.protocol_number_mapping import PROTOCOL_MAPPING_DICT

class Solution:
    def __init__(self):
        self.lookup_table = {}
        self.tag_count = defaultdict(int)
        self.port_protocol_count = defaultdict(int)

    def validate_file(self, filename):
        """
        Checks if the file path exists.
        Args:
            filename: The file which needs to be checked.
        Raises:
            FileNotFoundError: if file path does not exist
        """
        if not os.path.exists(filename):
            logger.error(f"File not found: {filename}")
            raise FileNotFoundError(f"File not found: {filename}")

    def validate_file_format(self, filename, expected_extension):
        """
        Validate the file extension.
        Args:
            filename: The file which needs to be checked.
            expected_extension: The extension which was expected for the particular filename.
        Raises:
            ValueError: If the file is of the wrong format.
        """
        if not filename.lower().endswith(expected_extension):
            logger.error(f"Invalid file format: {filename}. Expected a {expected_extension} file.")
            raise ValueError(f"Invalid file format: {filename}. Expected a {expected_extension} file.")
        logger.info(f"File format validated: {filename}")

    def read_lookup_table(self, filename):
        """
        Reads the lookup input file and stores it as a dictionary with (dstport, protocol) as keys and tag as the value.
        Args:
            filename: The lookup file to read.
        Raises:
            ValueError: If the file format is incorrect.
            FileNotFoundError: If the file does not exist.
            Exception: If there is an error reading the lookup file.
        """
        logger.info("Reading lookup table CSV file")
        try:
            self.validate_file(filename)
            self.validate_file_format(filename, VALID_LOOKUP_FILE_FORMAT)
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    dstport = row[DSTPORT_LOOKUP_KEY].strip().lower()
                    protocol = row[PROTOCOL_LOOKUP_KEY].strip().lower()
                    tag = row[TAG_LOOKUP_KEY].strip()
                    key = (dstport, protocol)
                    self.lookup_table[key] = tag
            logger.info("Lookup table loaded successfully")
        except FileNotFoundError as fnf_error:
            logger.error(f"FileNotFoundError: {fnf_error}")
            raise
        except ValueError as ve:
            logger.error(f"File validation error: {ve}")
            raise
        except Exception as e:
            logger.exception(f"Error reading lookup table: {e}")
            raise

    def process_flow_logs_file(self, flow_log_file):
        """
        Processes the flow log file to map entries based on destination port and protocol, updating tag counts and combination counts.
        Args:
            flow_log_file: The flow log file to process.
        Raises:
            ValueError: If the file format is incorrect.
            FileNotFoundError: If the file does not exist.
            Exception: If there is an error processing the flow log file.
        """
        logger.info("Processing flow log file")
        try:
            self.validate_file(flow_log_file)
            self.validate_file_format(flow_log_file, VALID_INPUT_FILE_FORMAT)
            with open(flow_log_file, mode='r') as file:
                for line in file:
                    fields = line.split()
                    if len(fields) < VERSION_2_FIELDS_COUNT:
                        logger.warning("Skipping incorrect log entry")
                        continue

                    dstport = fields[DSTPORT_FIELD_INDEX].strip().lower()
                    protocol_num = fields[PROTOCOL_FIELD_INDEX].strip().lower()
                    protocol = PROTOCOL_MAPPING_DICT.get(protocol_num, '-').lower()

                    if dstport == "-" or protocol == "-":
                        self.tag_count[UNTAGGED_LOOKUP_KEY] += 1
                        continue

                    key = (dstport, protocol)
                    if key in self.lookup_table:
                        tag = self.lookup_table[key]
                        self.tag_count[tag] += 1
                    else:
                        self.tag_count[UNTAGGED_LOOKUP_KEY] += 1
        
                    self.port_protocol_count[key] += 1
            logger.info("Flow log processing completed successfully")
        except FileNotFoundError as fnf_error:
            logger.error(f"FileNotFoundError: {fnf_error}")
            raise
        except ValueError as ve:
            logger.error(f"File validation error: {ve}")
            raise
        except Exception as e:
            logger.exception(f"Error processing flow log file: {e}")
            raise
    
    def create_output_file(self, output_file):
        """
        Writes the tag counts and port/protocol combination counts to the output file.
        Args:
            output_file: The file where the output should be written.
        Raises:
            ValueError: If the output file is not in the correct format.
            Exception: If there is an error writing the output file.
        """
        logger.info("Validating and writing output to file")
        try:
            self.validate_file_format(output_file, VALID_OUTPUT_FILE_FORMAT)
            with open(output_file, mode="w") as file:
                file.write("Tag Counts:\n")
                file.write(f"{'Tag':<12}{'Count':<12}\n")
                for tag, count in self.tag_count.items():
                    file.write(f"{tag:<12}{count:<12}\n")

                file.write("\nPort/Protocol Combination Counts:\n")
                file.write(f"{'Port':<12}{'Protocol':<12}{'Count':<12}\n")
                for (port, protocol), count in self.port_protocol_count.items():
                    file.write(f"{port:<12}{protocol:<12}{count:<12}\n")
            logger.info(f"Output written to {output_file} successfully")
        except ValueError as ve:
            logger.error(f"File validation error: {ve}")
            raise
        except Exception as e:
            logger.exception(f"Error writing output file: {e}")
            raise
