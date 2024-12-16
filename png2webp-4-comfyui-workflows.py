import os
import json
from PIL import Image
import pathlib

"""
    This class searches a specified directory for PNG images and converts them to the WebP format, 
    while preserving the metadata from the original ComfyUI workflow.
"""

class PngToWebPConverter:
    def __init__(self, directory, quality=90, method=6):
        self.directory = directory
        self.quality = quality
        self.method = method

    def save_webp(self, input_filename: str) -> dict:
        
        PROMPT_TAG = 0x0110  # Hexadecimal value for the tag where the prompt string is stored
        EXTRA_METADATA_TAG = 0x010f  # Hexadecimal value for additional metadata that is decremented

        # Load the input image and its metadata
        img = Image.open(input_filename)
        metadata = img.info

        # https://github.com/fernicar/png2webp_for_ComfyUI
        output_metadata = img.getexif()
        for key, value in metadata.items():
            if key == 'prompt':
                prompt_str = json.dumps(json.loads(value))
                output_metadata[PROMPT_TAG] = "Prompt:" + prompt_str
            elif key == 'workflow':
                workflow_str = json.dumps(json.loads(value))
                output_metadata[EXTRA_METADATA_TAG] = "Workflow:" + workflow_str
                EXTRA_METADATA_TAG -= 1
            else:
                value_str = json.dumps(json.loads(value))
                output_metadata[EXTRA_METADATA_TAG] = "{}:{}".format(key, value_str)
                EXTRA_METADATA_TAG -= 1
        exif_data = output_metadata

        # Create the output image
        output_img = img.convert('RGB')

        # Use the full PNG filename for the WebP file
        base_path = pathlib.Path(input_filename)
        output_path = base_path.with_suffix('.webp')
        
        # Save the output image, overwriting if it already exists
        output_img.save(output_path, exif=exif_data, quality=self.quality, method=self.method)

        return {
            "filename": output_path,
        }

    def convert(self):
        if not os.path.exists(self.directory):
            print(f"Error: {self.directory} does not exist")
            return

        for file in os.listdir(self.directory):
            if file.endswith('.png'):
                input_filename = os.path.join(self.directory, file)
                results = self.save_webp(input_filename)
                print(results)

if __name__ == "__main__":
    converter = PngToWebPConverter(directory="urPath2Dir")
    converter.convert()

    














