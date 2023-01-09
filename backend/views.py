import json
from urllib import response
from django.forms.models import model_to_dict
from django.http.response import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import os
from random import randint
import datetime
from django.core.mail import BadHeaderError, send_mail
from smtplib import SMTPRecipientsRefused
from django.core.files.storage import FileSystemStorage
import pandas as pd
from partial_date import PartialDate
#
from icalendar import Calendar, Event
# from datetime import datetime
# from pytz import UTC
# from .serializers import userSerializer
import time
from jose import jwt, jws
import requests

from backend.enable import keyEnable
#

from .models import costCategoryModel, costExpenseModel, costModel, expenseTypeModel, otpModel, reservationModel, sessionModel, settingsModel, adminModel
##########################################################################################################
##########################################################################################################
#
slapi = ""

@csrf_exempt
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        passw = request.POST.get("password")
        if email == None or passw == None:
            return JsonResponse({"error": "Invalid details."})
        users = adminModel.objects.filter(email=email)

        if len(users) == 0:
            return JsonResponse({"error": "User doesnot exists."})
        else:
            existsession = sessionModel.objects.filter(email=email)
            if len(existsession) != 0:
                existsession.delete()
            isCorrect = (passw == users[0].password)

            if isCorrect:
                try:
                    session = sessionModel()
                    tok = os.urandom(32)
                    tok = make_password(tok)
                    session.token = tok
                    session.email = email
                    session.tim = datetime.datetime.now()
                    session.save()
                    response = JsonResponse(
                        {"data": {"user_id": users[0].id}})
                    response.set_cookie("session_id_$cedar", tok)
                    return response
                except Exception as e:
                    print(e)
                    return JsonResponse({"error": "something went wrong."})
            else:
                return JsonResponse({"error": "Password wrong."})

    else:
        return JsonResponse({"error": "Method not allowed"})


@csrf_exempt
def logout(request):
    if request.method == "POST":
        sessionId = request.POST.get("sessionId")
        if sessionId == None:
            return JsonResponse({"code": "500", "error": "Invalid details."})

        if sessionId:
            try:
                sessionModel.objects.filter(token=sessionId).delete()
                response = JsonResponse({"code": "200", "data": "success"})
                response. delete_cookie('session_id_$cedar')
                return response
            except:
                return JsonResponse({"code": "500", "error": "something went wrong."})
        else:
            return JsonResponse({"code": "401", "error": "Not logged in."})
    else:
        return JsonResponse({"code": "400", "error": "Method not allowed"})


@csrf_exempt
def upload(request):
    if request.method == "POST":
        sessionId = request.POST.get("sessionId")
        if sessionId == None:
            return JsonResponse({"code": "500", "error": "Invalid details."})

        if isAdmin(sessionId):
            try:
                xlsx = request.FILES.get("xlsx")
                ics = request.FILES.get("ics")
                if xlsx and ics:
                    fs = FileSystemStorage()
                    filename = fs.save("xlsx/"+xlsx.name, xlsx)
                    filename1 = fs.save("ics/"+ics.name, ics)
                    # uploaded_file_url = fs.url(filename)
                    # uploaded_file_url1 = fs.url(filename1)
                    # print(uploaded_file_url, uploaded_file_url1)
                    empexceldata = pd.read_excel("media/"+filename)
                    dbframe = empexceldata
                    # print(dbframe.columns)
                    dbframe.rename(columns={'Reservation No': 'reservationNo',
                                            'Guest First Name': 'guestFirstName', 'Guest Last Name': 'guestLastName', 'Check-In date': 'checkInDate', 'Check-Out date': 'checkOutDate', 'Unit No': 'unitNo', 'Create Date': 'createDate'

                                            },
                                   inplace=True, errors='raise')
                    print(dbframe.columns)
                    for dbframe in dbframe.itertuples():
                        # print(dbframe)
                        tem = reservationModel.objects.filter(
                            reservationNo=dbframe.reservationNo)
                        if not len(tem):
                            obj = reservationModel()
                            obj.reservationNo = dbframe.reservationNo
                            obj.guestFirstName = dbframe.guestFirstName
                            obj.guestLastName = dbframe.guestLastName
                            obj.country = dbframe.Country
                            obj.email = dbframe.Email
                            obj.room = dbframe.Room
                            obj.unitNo = dbframe.unitNo
                            obj.subTotal = dbframe.Subtotal
                            obj.revenue = dbframe.Revenue
                            obj.currency = dbframe.Currency
                            obj.checkInDate = dbframe.checkInDate
                            obj.checkOutDate = dbframe.checkOutDate
                            # dbframe.checkInDate = dbframe.checkInDate.apply(pd.to_datetime)
                            # dbframe.checkOutDate = dbframe.checkOutDate.apply(pd.to_datetime)
                            obj.totalDays = (
                                dbframe.checkOutDate - dbframe.checkInDate).days
                            print((dbframe.checkOutDate -
                                  dbframe.checkInDate).days)
                            obj.createDate = dbframe.createDate
                            obj.save()

                    # with open("media/"+filename1, "r") as txt_file:
                    #     print(txt_file.readlines())

                    g = open("media/"+filename1, 'rb')
                    gcal = Calendar.from_ical(g.read())
                    for component in gcal.walk():
                        if component.name == "VEVENT":
                            val = component.get('summary')
                            val = val.split(",")
                            for i in val:
                                # print("i=>", i)
                                if "occupancy: " in i:
                                    rid = [p for p in val if "Reservation: " in p][0].replace(
                                        "Reservation: #", '')
                                    rid = int(rid)
                                    occ = [p for p in val if "occupancy: " in p][0].replace(
                                        " occupancy: adults/children (", '') .replace(')', '').split('/')
                                    adult = int(occ[0])
                                    child = int(occ[1])

                                    # print("rid=>", rid, occ)

                                    reservationModel.objects.filter(reservationNo=rid).update(
                                        adults=adult, children=child)

                                    rid = occ = []
                    g.close()
                    response = JsonResponse({"code": "200", "data": "success"})
                    return response
                else:
                    return JsonResponse({"code": "500", "error": "Invalid file."})

            except Exception as e:
                print(e)
                return JsonResponse({"code": "500", "error": "something went wrong."})
        else:
            return JsonResponse({"code": "401", "error": "Not logged in."})
    else:
        return JsonResponse({"code": "400", "error": "Method not allowed"})


@csrf_exempt
def createExpType(request):

    if request.method == "POST":
        sessionId = request.POST.get("sessionId")
        if sessionId == None:
            return JsonResponse({"code": "500", "error": "Invalid details."})

        if isAdmin(sessionId):

            try:
                cat = request.POST.get("category")
                typ = request.POST.get("type")
                print(cat, typ)
                if cat == None or typ == None:
                    return JsonResponse({"error": "Invalid data"})
                mod = expenseTypeModel()
                mod.typ = typ
                mod.category = costCategoryModel.objects.get(id=cat)
                mod.save()
                response = JsonResponse({"code": "200", "data": "success"})
                return response

            except Exception as e:
                print(e)
                return JsonResponse({"code": "500", "error": "something went wrong."})
        else:
            return JsonResponse({"code": "401", "error": "Not logged in."})
    else:
        return JsonResponse({"code": "400", "error": "Method not allowed"})


@csrf_exempt
def addExp(request):

    if request.method == "POST":
        sessionId = request.POST.get("sessionId")
        if sessionId == None:
            return JsonResponse({"code": "500", "error": "Invalid details."})

        if isAdmin(sessionId):

            try:
                date = request.POST.get("date")
                amount = request.POST.get("amount")
                expense = request.POST.get("expense")
                reciept = request.FILES.get("reciept")

                if date == None or amount == None or expense == None or reciept == None:
                    return JsonResponse({"error": "Invalid data"})
                # print("cat",)
                if expenseTypeModel.objects.get(id=expense).category.id == 1:

                    mod = costModel()
                    mod.date = PartialDate(date)
                    mod.amount = amount
                    # print(expenseTypeModel.objects.get(expense))
                    mod.expense = expenseTypeModel.objects.get(id=expense)
                    mod.reciept = reciept
                    mod.save()
                else:
                    mod = costExpenseModel()
                    mod.date = PartialDate(date)
                    mod.amount = amount
                    # print(expenseTypeModel.objects.get(expense))
                    mod.expense = expenseTypeModel.objects.get(id=expense)
                    mod.reciept = reciept
                    mod.save()
                response = JsonResponse({"code": "200", "data": "success"})
                return response

            except Exception as e:
                print(e)
                return JsonResponse({"code": "500", "error": "something went wrong."})
        else:
            return JsonResponse({"code": "401", "error": "Not logged in."})
    else:
        return JsonResponse({"code": "400", "error": "Method not allowed"})


@csrf_exempt
def deleteExp(request):

    if request.method == "POST":
        sessionId = request.POST.get("sessionId")
        if sessionId == None:
            return JsonResponse({"code": "500", "error": "Invalid details."})

        if isAdmin(sessionId):

            try:
                ide = request.POST.get("id")

                if ide == None:
                    return JsonResponse({"error": "Invalid data"})
                costModel.objects.get(id=ide).delete()
                response = JsonResponse({"code": "200", "data": "success"})
                return response

            except Exception as e:
                print(e)
                return JsonResponse({"code": "500", "error": "something went wrong."})
        else:
            return JsonResponse({"code": "401", "error": "Not logged in."})
    else:
        return JsonResponse({"code": "400", "error": "Method not allowed"})


@csrf_exempt
def deleteCapExp(request):

    if request.method == "POST":
        sessionId = request.POST.get("sessionId")
        if sessionId == None:
            return JsonResponse({"code": "500", "error": "Invalid details."})

        if isAdmin(sessionId):

            try:
                ide = request.POST.get("id")

                if ide == None:
                    return JsonResponse({"error": "Invalid data"})
                costExpenseModel.objects.get(id=ide).delete()
                response = JsonResponse({"code": "200", "data": "success"})
                return response

            except Exception as e:
                print(e)
                return JsonResponse({"code": "500", "error": "something went wrong."})
        else:
            return JsonResponse({"code": "401", "error": "Not logged in."})
    else:
        return JsonResponse({"code": "400", "error": "Method not allowed"})


@csrf_exempt
def addNote(request):

    if request.method == "POST":
        sessionId = request.POST.get("sessionId")
        if sessionId == None:
            return JsonResponse({"code": "500", "error": "Invalid details."})

        if isAdmin(sessionId):

            try:
                ide = request.POST.get("id")
                note = request.POST.get("note")

                if ide == None or note == None:
                    return JsonResponse({"error": "Invalid data"})

                mod = reservationModel.objects.filter(id=ide)
                if not mod:
                    return JsonResponse({"error": "Invalid id"})
                mod.update(notes=note)

                response = JsonResponse({"code": "200", "data": "success"})
                return response

            except Exception as e:
                print(e)
                return JsonResponse({"code": "500", "error": "something went wrong."})
        else:
            return JsonResponse({"code": "401", "error": "Not logged in."})
    else:
        return JsonResponse({"code": "400", "error": "Method not allowed"})


@csrf_exempt
def enableKey(request):

    if request.method == "POST":
        sessionId = request.POST.get("sessionId")
        if sessionId == None:
            return JsonResponse({"code": "500", "error": "Invalid details."})

        if isAdmin(sessionId):

            try:
                ide = request.POST.get("id")

                if ide == None:
                    return JsonResponse({"error": "Invalid data"})

                mod = reservationModel.objects.filter(id=ide)
                if not mod:
                    return JsonResponse({"error": "Invalid id"})
                ret1, ret2 = keyEnable(mod[0])
                # print()
                if "error" in ret1 :
                    return JsonResponse({"code": "400", "error": ret1['message']})
                if "error" in ret2 :
                    return JsonResponse({"code": "400", "error": ret2['message']})
                mod.update(klevioKey=True)
                response = JsonResponse({"code": "200", "data": "success"})
                return response

            except Exception as e:
                print("Here----",e)
                return JsonResponse({"code": "500", "error": "something went wrong."})
        else:
            return JsonResponse({"code": "401", "error": "Not logged in."})
    else:
        return JsonResponse({"code": "400", "error": "Method not allowed"})


#####################################################################################


def isAdmin(sessionId):
    session = sessionModel.objects.filter(token=sessionId)
    if len(session) != 0:
        try:
            user = adminModel.objects.filter(email=session[0].email)
            if len(user):
                return True
            else:
                return False
        except:
            return False
    else:
        return False
