from googletrans import Translator
from .models import CropPrice

# Function to translate text to Kannada
def translate_to_kannada(text):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest='kn')
    return translated_text.text

# Retrieve all CropPrice objects
crop_prices = CropPrice.objects.all()

# Iterate through each CropPrice object
for crop_price in crop_prices:
    # Translate the crop name to Kannada
    translated_crop_name = translate_to_kannada(crop_price.crop_name)
    
    # Update the crop name with the translated one
    crop_price.crop_name = translated_crop_name
    
    # Save the changes
    crop_price.save()

print("Crop names translated and updated successfully!")
