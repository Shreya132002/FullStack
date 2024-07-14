from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse


# members/views.py
from googletrans import Translator
from .scripts.nlp_new import extract_keyword
from .scripts.voice_query_script import process_voice_query,speak,get_crop_price_english,translate_to_kannada,query,speak

def members(request):
    return HttpResponse("Hello World!")

# Create your views here.
# def voice_query(request):
#     if request.method == 'POST':
#         result = process_voice_query()
#         return render(request, 'members/voice_query.html', {'result': result})

    
#     return render(request, 'members/voice_query.html')

from .models import CropPrice

def crop(request):

    crop_prices = CropPrice.objects.all()
    print(crop_prices)
    # a=crop_prices[0]
    # print(a.crop_name)
    # translator = Translator()
    # translation = translator.translate(a.crop_name, dest='kn')
    # translated_text = translation.text
    # print(translated_text)
    


    return render(request, 'members/price_list.html', {'crop_prices': crop_prices})

# members/views.py




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
       return render(request,'members/voice_new.html',) 


from django.http import JsonResponse
from googletrans import Translator

def voice_query2(request):
    if request.method == 'POST':
        # Handle the audio file and text here
        audio_file = request.FILES.get('audio_blob')  # Get the uploaded audio file
        audio_text = request.POST.get('audio_text')  # Get the transcribed text
        # Translate the transcribed text
        print(audio_text)
        translator = Translator()
        translation = translator.translate(audio_text, dest='en')
        translated_text = translation.text
        
        key=extract_keyword(translated_text)
        print(key)
        if not key:
            speak("ಮತ್ತೊಮ್ಮೆ  ಸರಿಯಾಗಿ ಹೇಳಿ")
            result="ಸರಿಯಾಗಿ ಹೇಳಿ"
            return JsonResponse({'message': 'Audio file and transcribed text received and processed successfully.', 'translated_text': result})
        keyword=key[0]
        print(keyword)
        print(translate_to_kannada(keyword))
        
        # result = query(keyword)
        result = get_crop_price_english(keyword)
        print(result)
        
        
        
        # Return a JSON response with the translated text
        return JsonResponse({'message': 'Audio file and transcribed text received and processed successfully.', 'translated_text': result})
    else:
        # Handle other request methods if needed
        return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)

# views.py

from django.http import JsonResponse

def handle_table_data(request):
    if request.method == 'POST':
        crop_name = request.POST.get('crop_name')
        modal_price = request.POST.get('modal_price')
        onekg=float(modal_price)/100
        onekg=str(onekg)
        # Print the crop name and modal price in the backend
        print("Crop Name:", crop_name)
        print("Modal Price:", modal_price)
        speak(f"{crop_name} ಬೆಲೆ: {modal_price} ರೂಪಾಯಿ ಮತ್ತು 1 ಕಿಲೋಗ್ರಾಂಗಾಗಿ {onekg} ರೂಪಾಯಿ")

        # Optionally, you can return a response back to the frontend
        return JsonResponse({'status': 'success', 'message': 'Data received successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    




from django.shortcuts import render
from django.http import JsonResponse
def add(request):
       return render(request,'members/add_crop.html',) 

def add_crop(request):
    success_message = None
    if request.method == 'POST':
        name = request.POST.get('cropName')
        price = request.POST.get('cropPrice')
        print(name)
        print(price)
        if name and price:

            k_price = translate_to_kannada(price)
            k_name = translate_to_kannada(name)
            print(k_name)
            print(k_price)
            CropPrice.objects.create(crop_name=k_name, modal_price=k_price)
            success_message = 'Crop added successfully.'
        else:
            success_message = 'Crop name and price are required.'
    return render(request, 'members/add_crop.html', {'success_message': success_message})
