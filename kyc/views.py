from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
# import numpy as np
import urllib
import json
# import cv2
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from .forms import ImageUploadForm
from .models import ImageUploadModel
# import our OCR function
# from .ocr import ocr
# from .ocr1 import ocr1
from django.contrib.auth.decorators import login_required 

@login_required
def ocr_core(request):
    try:
        model = ImageUploadModel.objects.get(user=request.user.username)
    except Exception as e:
        model = 'blank'
    if model != 'blank':
        imageURLAF = model.imageAF.url
        imageURLAB = model.imageAB.url
        desc = model.description
        model.name = request.user.name
        model.user = request.user.username
        model.save()
    else:
        imageURLP = ""
        imageURLAF = ""
        imageURLAB = ""
        desc = ""
    

    if request.method == 'POST':
        try:
            user = request.user
            try:
                a = ImageUploadModel.objects.get(user=request.user.username)
            except Exception as e:
                a = 'blank'
            if a != 'blank':
                form = ImageUploadForm(request.POST, request.FILES, instance=a)
            else:
                form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()

                model = ImageUploadModel.objects.get(user=request.user.username)
                model.approved = None
                model.description = "Hurray! We are processing"
                model.name = request.user.name
                model.save()
                imageURLAF = model.imageAF.url
                imageURLAB = model.imageAB.url    

                # try:
                #     extracted_textp = ocr(imageURLP)
                #     extracted_textaf = ocr1(imageURLAF)
                #     extracted_textab = ocr1(imageURLAB)
                #     if extracted_textp.get('Name') in str(extracted_textaf).upper():
                #         model.pan = extracted_textp.get('pan')
                #         model.save()
                #         extracted_text="Hurray! KYC got verified..."
                #         user = request.user
                #         user.kyc_verified = True
                #         user.save()
                #     else:
                #         extracted_text="Not Verified, Please Try Again with clearer images!"
                # except Exception as e:
                #     extracted_text = "Something went wrong {}".format(e)
        except Exception as e:
            extracted_text = "Error 500 {}".format(e)


            return render(request, 'pcard/pcard.html', {'form':form, 'model': model, 'post':post, 'extracted_text': extracted_text, 'imagep': imageURLP, 'imageaf': imageURLAF, 'imageab': imageURLAB, })
    else:
        form = ImageUploadForm()
    return render(request, 'pcard/pcard.html',{'form':form, 'model': model, 'desc': desc, 'imageaf': imageURLAF, 'imageab': imageURLAB,})