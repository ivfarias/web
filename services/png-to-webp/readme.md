# PNG to WebP Converter

This Python script reads PNG files from the `/inputs` folder and converts them to WebP format, saving the converted files into the `/outputs` folder. It uses the Pillow library for image processing.

## Prerequisites

- Python 3.x
- Pillow library

## Installation

1. Clone the repository or download the script `converter.py` to your local machine.
2. Create a virtual environment (optional, but highly recommended): `python3 -m venv venv source venv/bin/activate`
3. Install the Pillow library by running the following command:
`pip install pillow` or `pip install -r requirements.txt` if you cloned the repository.

## Usage

1. Place the PNG files you want to convert inside the `/inputs` folder.
2. Run the script `python3 converter.py`.
3. The script will convert the PNG files to WebP format and save them in the `/outputs` folder.
4. After the script finishes running, you can find the converted WebP files in the `/outputs` folder.

**Note**: If the `/outputs` folder does not exist, the script will create it automatically.

## Customization

- If you want to use different input and output folder paths, you can update the `input_folder` and `output_folder` variables in the script.

## License

This project is licensed under the [MIT License](LICENSE).
