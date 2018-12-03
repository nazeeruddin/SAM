# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse

from django.shortcuts import render

from AI_Class_and_Object_Implementation import Email_AI
from duckling_simplified import Parse_date_duckling
from memory import memory, update_report_id

ai = Email_AI()
ai.fit_classifier()

# Create your views here.
def index(request):

    return render(request, 'test.html')

def bot(request):

    Report_ID = 0
    userText = request.GET.get('msg', False)

    if userText.lower() == 'hi' or userText.lower() == 'hello':
        return HttpResponse('Hi There.')
    if userText.lower() == 'how are you':
        return HttpResponse("I'm Good, Thanks for Asking")
    if userText.lower() == 'are you human':
        return HttpResponse("No, I am a Chat Bot, Your Personal Sales Assistant :)")
    if 'bye' in userText.lower():
        return HttpResponse("Bye, Thank You.")

    grain, date, end_date, date_string = Parse_date_duckling(userText)

    if Report_ID == 0 and date is not None:
        try:
            id = str(memory())
            if int(id) != 0:
                update_report_id(0)
                return HttpResponse('Report Id:' + str(id))
        except Exception as e:
            return HttpResponse("I Can't Answer This Query.")

    Report_ID, self_flag, date1, end_date1, ai_input_string, confidence = ai.user_input(userText)

    if int(confidence) < 70.0:
        return HttpResponse("I Can't Answer This Query.")
    try:
        if date is not None:
            date = str(date).split('T')[0]
    except:
        pass
    if date is None or date == 'None':
        # return 'For Which Date You are Looking for?'
        update_report_id(Report_ID)
        return HttpResponse("For Which Date You are Looking for?")
    # return ' Report Id: '+str(Report_ID)+' and Date: '+str(date)
    return HttpResponse(' Report Id: ' + str(Report_ID))