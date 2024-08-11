import argparse
from solution.solution import Solution
from common.logger import logger

def main():
    parser = argparse.ArgumentParser(description="Process flow logs and map them to tags based on a lookup table.")
    parser.add_argument(
        "--lookup-file",
        "-l",
        required=True,
        type=str,
        help="Path to the lookup table csv file."
    )
    parser.add_argument(
        "--input-file",
        "-i",
        required=True,
        type=str,
        help="Path to the flow log txt file."
    )
    parser.add_argument(
        "--output-file",
        "-o",
        required=True,
        type=str,
        help="Path to the output txt file. Must have a .txt extension."
    )

    args = parser.parse_args()

    solution = Solution()
    solution.read_lookup_table(args.lookup_file)
    solution.process_flow_logs_file(args.input_file)
    solution.create_output_file(args.output_file)
    logger.info("Program completed successfully")

if __name__ == "__main__":
    main()
