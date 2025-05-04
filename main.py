import os
import json
import xml.etree.ElementTree as ET
from model_processor.xml_parser import XmlModelParser
from model_processor.config_generator import ConfigGenerator
from model_processor.delta_processor import DeltaProcessor


def ensure_output_dir():
    os.makedirs("out", exist_ok=True)


def write_json_to_file(data, filename, indent=4):
    with open(filename, "w") as f:
        json.dump(data, f, indent=indent)


def main():
    ensure_output_dir()

    try:
        print("Parsing XML model...")
        parser = XmlModelParser("impulse_test_input.xml")
        class_model = parser.parse()

        generator = ConfigGenerator(class_model)

        print("Generating config.xml...")
        with open("out/config.xml", "w") as f:
            f.write(generator.generate_config_xml())

        print("Generating meta.json...")
        write_json_to_file(generator.generate_meta_json(), "out/meta.json")

        print("Processing configuration deltas...")
        delta_processor = DeltaProcessor("config.json", "patched_config.json")

        print("Generating delta.json...")
        write_json_to_file(
            json.loads(delta_processor.generate_delta()), "out/delta.json"
        )

        print("Generating res_patched_config.json...")
        write_json_to_file(
            json.loads(delta_processor.apply_delta()), "out/res_patched_config.json"
        )

        print("Successfully generated all output files in the 'out' directory")

    except FileNotFoundError as e:
        print(f"Error: Missing input file - {str(e)}")
    except ET.ParseError:
        print("Error: Invalid XML format in input file")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in input file")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
