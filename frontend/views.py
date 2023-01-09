import json
from warnings import catch_warnings
from django.forms.models import model_to_dict
from django.http.response import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import calendar
from datetime import datetime
from django.db.models import Q
from django.db.models import Sum
#
from backend.models import costCategoryModel, costExpenseModel, costModel, expenseTypeModel, reservationModel, settingsModel, adminModel, sessionModel
from backend.serializers import costSerializer
# from backend.serializers import candidateSerializer, userSerializer
# from backend.views import getAdmin, getUser, isAdmin, isUser
##########################################################################################################
##########################################################################################################


@csrf_exempt
def loginView(request):
    sessionId = request.COOKIES.get("session_id_$cedar")
    if sessionId:
        return HttpResponseRedirect('/dashboard')
    settings = settingsModel.objects.all()[0]
    return render(request,  "login.html", {"settings": settings})


# @csrf_exempt
# def dashboardView(request):
#     sessionId = request.COOKIES.get("session_id_$cedar")
#     if not sessionId:
#         return HttpResponseRedirect('/')
#     settings = settingsModel.objects.all()[0]
#     sess = sessionModel.objects.filter(token=sessionId)
#     # print("user--",sess)
#     user = adminModel.objects.filter(
#         email=sess[0].email)

#     return render(request,  "admin.html", {"settings": settings, "page_name": "Dashboard", "name": user[0].name})


@csrf_exempt
def dashboardView(request):
    return HttpResponseRedirect('/monthly/')





@csrf_exempt
def mapView(request):
    sessionId = request.COOKIES.get("session_id_$cedar")
    if not sessionId:
        return HttpResponseRedirect('/')
    settings = settingsModel.objects.all()[0]
    sess = sessionModel.objects.filter(token=sessionId)
    # print("user--",sess)
    user = adminModel.objects.filter(
        email=sess[0].email)

    return render(request,  "map.html", {"settings": settings, "page_name": "Map", "name": user[0].name})


@csrf_exempt
def calendarView(request):
    sessionId = request.COOKIES.get("session_id_$cedar")
    if not sessionId:
        return HttpResponseRedirect('/')
    settings = settingsModel.objects.all()[0]
    sess = sessionModel.objects.filter(token=sessionId)
    # print("user--",sess)
    user = adminModel.objects.filter(
        email=sess[0].email)

    return render(request,  "calander.html", {"settings": settings, "page_name": "Calendar", "name": user[0].name})


@csrf_exempt
def uploadView(request):
    sessionId = request.COOKIES.get("session_id_$cedar")
    if not sessionId:
        return HttpResponseRedirect('/')
    settings = settingsModel.objects.all()[0]
    sess = sessionModel.objects.filter(token=sessionId)
    # print("user--",sess)
    user = adminModel.objects.filter(
        email=sess[0].email)

    return render(request,  "upload.html", {"settings": settings, "page_name": "Upload data", "name": user[0].name})


@csrf_exempt
def costsView(request):
    sessionId = request.COOKIES.get("session_id_$cedar")
    if not sessionId:
        return HttpResponseRedirect('/')
    settings = settingsModel.objects.all()[0]
    sess = sessionModel.objects.filter(token=sessionId)
    # print("user--",sess)
    user = adminModel.objects.filter(
        email=sess[0].email)
    costCat = list(
        costCategoryModel.objects.all().order_by("category").values())
    expType = list(expenseTypeModel.objects.all().order_by("typ").values())

    fromYear = request.GET.get("fromYear")
    fromMonth = request.GET.get("fromMonth")
    toYear = request.GET.get("toYear")
    toMonth = request.GET.get("toMonth")
    # print(fromYear,fromMonth, toYear, toMonth)
    if fromYear == None or fromMonth == None or toYear == None or toMonth == None:
        allCosts = costSerializer(costModel.objects.all(), many=True).data
    else:
        fromDate = fromYear+"-"+fromMonth
        toDate = toYear+"-"+toMonth
        print(fromDate, toDate)
        allCosts = costModel.objects.filter(
            date__gte=fromDate).filter(date__lte=toDate)
        print(costModel.objects.all()[0].expense_id)
        allCosts = costSerializer(allCosts, many=True).data
    # print(allCosts)

    return render(request,  "costs.html", {"fromYear": fromYear, "fromMonth": fromMonth, "toYear": toYear, "toMonth": toMonth, "all_costs": allCosts, "exp_type": expType, "cost_cat": costCat, "settings": settings, "page_name": "Costs", "name": user[0].name})


@csrf_exempt
def capitalView(request):
    sessionId = request.COOKIES.get("session_id_$cedar")
    if not sessionId:
        return HttpResponseRedirect('/')
    settings = settingsModel.objects.all()[0]
    sess = sessionModel.objects.filter(token=sessionId)
    # print("user--",sess)
    user = adminModel.objects.filter(
        email=sess[0].email)
    costCat = list(
        costCategoryModel.objects.all().order_by("category").values())
    expType = list(expenseTypeModel.objects.all().order_by("typ").values())

    fromYear = request.GET.get("fromYear")
    fromMonth = request.GET.get("fromMonth")
    toYear = request.GET.get("toYear")
    toMonth = request.GET.get("toMonth")
    # print(fromYear,fromMonth, toYear, toMonth)
    if fromYear == None or fromMonth == None or toYear == None or toMonth == None:
        allCosts = costSerializer(
            costExpenseModel.objects.all(), many=True).data
    else:
        fromDate = fromYear+"-"+fromMonth
        toDate = toYear+"-"+toMonth
        print(fromDate, toDate)
        allCosts = costExpenseModel.objects.filter(
            date__gte=fromDate).filter(date__lte=toDate)
        # print(type(costModel.objects.all()[0].date),costModel.objects.all()[0].date)
        allCosts = costSerializer(allCosts, many=True).data
    # print(allCosts)

    return render(request,  "capital.html", {"fromYear": fromYear, "fromMonth": fromMonth, "toYear": toYear, "toMonth": toMonth, "all_costs": allCosts, "exp_type": expType, "cost_cat": costCat, "settings": settings, "page_name": "Capital Expenditure", "name": user[0].name})


@csrf_exempt
def cleaningView(request):
    sessionId = request.COOKIES.get("session_id_$cedar")
    if not sessionId:
        return HttpResponseRedirect('/')
    settings = settingsModel.objects.all()[0]
    sess = sessionModel.objects.filter(token=sessionId)
    # print("user--",sess)
    user = adminModel.objects.filter(
        email=sess[0].email)

    year = request.GET.get("year")
    month = request.GET.get("month")

    if year == None or month == None:
        allReserve = []

    else:
        year = int(year)
        month = int(month)
        d_fmt = "{0:>02}.{1:>02}.{2}"
        date_from = datetime.strptime(
            d_fmt.format(1, month, year), '%d.%m.%Y').date()
        last_day_of_month = calendar.monthrange(year, month)[1]
        date_to = datetime.strptime(
            d_fmt.format(last_day_of_month, month, year), '%d.%m.%Y').date()
        allReserve = list(reservationModel.objects.filter(
            Q(checkInDate__gte=date_from)
            &
            Q(checkInDate__lte=date_to)).values())

        # allReserve = costSerializer(allReserve, many=True).data

    return render(request,  "cleaning.html", {"year": year, "month": month, "all_reserve": allReserve, "settings": settings, "page_name": "Cleaning", "name": user[0].name})





@csrf_exempt
def monthlyView(request):
    sessionId = request.COOKIES.get("session_id_$cedar")
    if not sessionId:
        return HttpResponseRedirect('/')
    settings = settingsModel.objects.all()[0]
    sess = sessionModel.objects.filter(token=sessionId)
    # print("user--",sess)
    user = adminModel.objects.filter(
        email=sess[0].email)

    year = request.GET.get("year")
    month = request.GET.get("month")

    if year == None or month == None:
        allReserve = []

    else:
        year = int(year)
        month = int(month)
        d_fmt = "{0:>02}.{1:>02}.{2}"
        date_from = datetime.strptime(
            d_fmt.format(1, month, year), '%d.%m.%Y').date()
        last_day_of_month = calendar.monthrange(year, month)[1]
        date_to = datetime.strptime(
            d_fmt.format(last_day_of_month, month, year), '%d.%m.%Y').date()
        allReserve = list(reservationModel.objects.filter(
            Q(checkInDate__gte=date_from)
            &
            Q(checkInDate__lte=date_to)).values())

        # allReserve = costSerializer(allReserve, many=True).data

    return render(request,  "monthly.html", {"year": year, "month": month, "all_reserve": allReserve, "settings": settings, "page_name": "Monthly data", "name": user[0].name})


@csrf_exempt
def keysView(request):
    sessionId = request.COOKIES.get("session_id_$cedar")
    if not sessionId:
        return HttpResponseRedirect('/')
    settings = settingsModel.objects.all()[0]
    sess = sessionModel.objects.filter(token=sessionId)
    # print("user--",sess)
    user = adminModel.objects.filter(
        email=sess[0].email)

    year = request.GET.get("year")
    month = request.GET.get("month")

    if year == None or month == None:
        allReserve = []

    else:
        year = int(year)
        month = int(month)
        d_fmt = "{0:>02}.{1:>02}.{2}"
        date_from = datetime.strptime(
            d_fmt.format(1, month, year), '%d.%m.%Y').date()
        last_day_of_month = calendar.monthrange(year, month)[1]
        date_to = datetime.strptime(
            d_fmt.format(last_day_of_month, month, year), '%d.%m.%Y').date()
        allReserve = list(reservationModel.objects.filter(
            Q(checkInDate__gte=date_from)
            &
            Q(checkInDate__lte=date_to)).values())

        # allReserve = costSerializer(allReserve, many=True).data

    return render(request,  "keys.html", {"year": year, "month": month, "all_reserve": allReserve, "settings": settings, "page_name": "Key management", "name": user[0].name})


@csrf_exempt
def revenueView(request):
    sessionId = request.COOKIES.get("session_id_$cedar")
    if not sessionId:
        return HttpResponseRedirect('/')
    settings = settingsModel.objects.all()[0]
    sess = sessionModel.objects.filter(token=sessionId)
    # print("user--",sess)
    user = adminModel.objects.filter(
        email=sess[0].email)

    typ = request.GET.get("type")
    # year = request.GET.get("year")
    plot = request.GET.get("plot")

    if plot == None or typ == None:
        return render(request,  "revenue.html", {"plot": plot, "type": typ,  "all_reserve": [], "settings": settings, "page_name": "Revenue", "name": user[0].name})
    else:
        typ = int(typ)
        plot = int(plot)
        if typ == 0:
            year = request.GET.get("year")
            year = int(year)
            d_fmt = "{0:>02}.{1:>02}.{2}"
            date_from = datetime.strptime(
                d_fmt.format(1, 1, year), '%d.%m.%Y').date()
            date_to = datetime.strptime(
                d_fmt.format(31, 12, year), '%d.%m.%Y').date()
            allReserve = reservationModel.objects.filter(
                Q(checkInDate__gte=date_from)
                &
                Q(checkInDate__lte=date_to))
            res = []
            totInc = 0
            tD = 0
            for i in range(1, 13):
                date_from = datetime.strptime(
                    d_fmt.format(1, i, year), '%d.%m.%Y').date()
                last_day_of_month = calendar.monthrange(year, i)[1]
                date_to = datetime.strptime(
                    d_fmt.format(last_day_of_month, i, year), '%d.%m.%Y').date()
                allReserveTemp = allReserve.filter(
                    Q(checkInDate__gte=date_from)
                    &
                    Q(checkInDate__lte=date_to))
                totDays = allReserveTemp.aggregate(Sum('totalDays'))[
                    'totalDays__sum']
                if totDays == None:
                    totDays = 0
                try:
                    occ = round((totDays/last_day_of_month)*100, 1)
                except:
                    occ = 0
                inc = allReserveTemp.aggregate(Sum('revenue'))['revenue__sum']
                if not inc:
                    inc = 0
                tD += totDays
                totInc += inc
                res.append({"Month": calendar.month_name[i], "TotalDays": totDays, "NumberOfBooking": len(
                    allReserveTemp), "AverageLength":  round(totDays/len(allReserveTemp),1), "TotalIncome": inc, "Occupancy": occ})

            # print(res)
            totCos1 = costModel.objects.filter(
                date__gte=str(year)+"-01").filter(date__lte=str(year)+"-12").aggregate(Sum('amount'))['amount__sum']

            totCos2 = costExpenseModel.objects.filter(
                date__gte=str(year)+"-01").filter(date__lte=str(year)+"-12").aggregate(Sum('amount'))['amount__sum']
            if not totCos1:
                totCos1 = 0
            if not totCos2:
                totCos2 = 0
            # totCos = totCos1+totCos2
            profit = totInc - totCos1

            return render(request,  "revenue.html", {"plot": plot, "capExp": totCos2, "occupancy": round((tD/356)*100, 1), "totPro": profit, "totCos": totCos1, "totInc": totInc, "type": 0, "year": year, "all_reserve": res, "settings": settings, "page_name": "Revenue", "name": user[0].name})
        elif typ == 1:
            fromYear = request.GET.get("fromYear")
            toYear = request.GET.get("toYear")
            fromMonth = request.GET.get("fromMonth")
            toMonth = request.GET.get("toMonth")
            d_fmt = "{0:>02}.{1:>02}.{2}"
            date_from = datetime.strptime(
                d_fmt.format(1, fromMonth, fromYear), '%d.%m.%Y').date()
            last_day_of_month = calendar.monthrange(
                int(toYear), int(toMonth))[1]
            date_to = datetime.strptime(
                d_fmt.format(last_day_of_month, toMonth, toYear), '%d.%m.%Y').date()
            allReserve = reservationModel.objects.filter(
                Q(checkInDate__gte=date_from)
                &
                Q(checkInDate__lte=date_to))
            res = []
            totInc = 0
            tD = 0

            sd = datetime.strptime(
                str(fromYear)+"-"+str(fromMonth)+"-01", "%Y-%m-%d")
            ed = datetime.strptime(
                str(toYear)+'-'+str(toMonth)+'-'+str(last_day_of_month), "%Y-%m-%d")

            lst = [datetime.strptime('%2.2d-%2.2d' % (y, m), '%Y-%m').strftime('%B-%Y')
                   for y in range(sd.year, ed.year+1)
                   for m in range(sd.month if y == sd.year else 1, ed.month+1 if y == ed.year else 13)]

            # print(lst)
            months_in_year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            for i in lst:
                # print(i)
                date_from = datetime.strptime(
                    d_fmt.format(1,  i.split('-')[0], i.split('-')[1]), '%d.%B.%Y').date()
                # print(date_from)

                last_day_of_month = calendar.monthrange(int(i.split('-')[1]), months_in_year.index(i.split('-')[0])+1)[1]
                # print(last_day_of_month)
                date_to = datetime.strptime(
                    d_fmt.format(last_day_of_month, i.split('-')[0], i.split('-')[1]), '%d.%B.%Y').date()
                # print(date_to)
                allReserveTemp = allReserve.filter(
                    Q(checkInDate__gte=date_from)
                    &
                    Q(checkInDate__lte=date_to))
                totDays = allReserveTemp.aggregate(Sum('totalDays'))[
                    'totalDays__sum']
                if totDays == None:
                    totDays = 0
                try:
                    occ = round((totDays/last_day_of_month)*100, 1)
                except:
                    occ = 0
                inc = allReserveTemp.aggregate(Sum('revenue'))['revenue__sum']
                if not inc:
                    inc = 0
                tD += totDays
                totInc += inc
                totCo = costModel.objects.filter(
                    date=str(i.split('-')[1])+"-"+str(months_in_year.index(i.split('-')[0])+1)).aggregate(Sum('amount'))['amount__sum']
                # print("TO-->>",totCo)
                if not totCo:
                    totCo = 0
                ii = i.split('-')
                res.append({"Date": ii[0][:3]+'-'+ii[1][-2:], "TotalCost": totCo,"Profit":inc - totCo, "TotalDays": totDays, "NumberOfBooking": len(
                    allReserveTemp), "TotalIncome": inc, "Occupancy": occ})

            print(res)
            totCos1 = costModel.objects.filter(
                date__gte=str(fromYear)+"-"+fromMonth).filter(date__lte=str(toYear)+"-"+toMonth).aggregate(Sum('amount'))['amount__sum']

            totCos2 = costExpenseModel.objects.filter(
                date__gte=str(fromYear)+"-"+fromMonth).filter(date__lte=str(toYear)+"-"+toMonth).aggregate(Sum('amount'))['amount__sum']
            if not totCos1:
                totCos1 = 0
            if not totCos2:
                totCos2 = 0
            # totCos = totCos1+totCos2
            profit = totInc - totCos1

            return render(request,  "revenue.html", {"plot": plot, "capExp": totCos2, "occupancy": round((tD/356)*100, 1), "totPro": profit, "totCos": totCos1, "totInc": totInc, "type": 1, "tomonth": toMonth, "frommonth": fromMonth, "toyear": toYear,  "fromyear": fromYear, "all_reserve": res, "settings": settings, "page_name": "Revenue", "name": user[0].name})
        else:
            return render(request,  "revenue.html", {"plot": plot, "type": typ, "tomonth": toMonth, "frommonth": fromMonth, "toyear": toYear,  "fromyear": fromYear, "all_reserve": [], "settings": settings, "page_name": "Revenue", "name": user[0].name})





@csrf_exempt
def taxView(request):
    sessionId = request.COOKIES.get("session_id_$cedar")
    if not sessionId:
        return HttpResponseRedirect('/')
    settings = settingsModel.objects.all()[0]
    sess = sessionModel.objects.filter(token=sessionId)
    # print("user--",sess)
    user = adminModel.objects.filter(
        email=sess[0].email)

    typ = request.GET.get("type")
    # year = request.GET.get("year")
    plot = request.GET.get("plot")

    if plot == None or typ == None:
        return render(request,  "tax.html", {"plot": plot, "type": typ,  "all_reserve": [], "settings": settings, "page_name": "Tax summary", "name": user[0].name})
    else:
        typ = int(typ)
        plot = int(plot)

        fromYear = request.GET.get("fromYear")
        toYear = request.GET.get("toYear")
        fromMonth = request.GET.get("fromMonth")
        toMonth = request.GET.get("toMonth")
        d_fmt = "{0:>02}.{1:>02}.{2}"
        date_from = datetime.strptime(
            d_fmt.format(1, fromMonth, fromYear), '%d.%m.%Y').date()
        last_day_of_month = calendar.monthrange(
            int(toYear), int(toMonth))[1]
        date_to = datetime.strptime(
            d_fmt.format(last_day_of_month, toMonth, toYear), '%d.%m.%Y').date()
        allReserve = reservationModel.objects.filter(
            Q(checkInDate__gte=date_from)
            &
            Q(checkInDate__lte=date_to))
        res = []
        totInc = 0
        tD = 0

        sd = datetime.strptime(
            str(fromYear)+"-"+str(fromMonth)+"-01", "%Y-%m-%d")
        ed = datetime.strptime(
            str(toYear)+'-'+str(toMonth)+'-'+str(last_day_of_month), "%Y-%m-%d")

        lst = [datetime.strptime('%2.2d-%2.2d' % (y, m), '%Y-%m').strftime('%B-%Y')
                for y in range(sd.year, ed.year+1)
                for m in range(sd.month if y == sd.year else 1, ed.month+1 if y == ed.year else 13)]

        # print(lst)
        months_in_year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        for i in lst:
            # print(i)
            date_from = datetime.strptime(
                d_fmt.format(1,  i.split('-')[0], i.split('-')[1]), '%d.%B.%Y').date()
            # print(date_from)

            last_day_of_month = calendar.monthrange(int(i.split('-')[1]), months_in_year.index(i.split('-')[0])+1)[1]
            # print(last_day_of_month)
            date_to = datetime.strptime(
                d_fmt.format(last_day_of_month, i.split('-')[0], i.split('-')[1]), '%d.%B.%Y').date()
            # print(date_to)
            allReserveTemp = allReserve.filter(
                Q(checkInDate__gte=date_from)
                &
                Q(checkInDate__lte=date_to))
            totDays = allReserveTemp.aggregate(Sum('totalDays'))[
                'totalDays__sum']
            if totDays == None:
                totDays = 0
            try:
                occ = round((totDays/last_day_of_month)*100, 1)
            except:
                occ = 0
            inc = allReserveTemp.aggregate(Sum('revenue'))['revenue__sum']
            if not inc:
                inc = 0
            tD += totDays
            totInc += inc
            totCo = costModel.objects.filter(
                date=str(i.split('-')[1])+"-"+str(months_in_year.index(i.split('-')[0])+1)).aggregate(Sum('amount'))['amount__sum']
            varCos = costExpenseModel.objects.filter(
                date=str(i.split('-')[1])+"-"+str(months_in_year.index(i.split('-')[0])+1)).aggregate(Sum('amount'))['amount__sum']
            # print("TO-->>",totCo)
            if not totCo:
                totCo = 0
            if not varCos:
                varCos = 0
            ii = i.split('-')
            res.append({"Date": ii[0][:3]+'-'+ii[1][-2:],"GrossProfit":inc-varCos, "VariableCost":varCos,"TotalCost": totCo,"Profit":inc - totCo, "TotalDays": totDays, "NumberOfBooking": len(
                allReserveTemp), "TotalIncome": inc, "Occupancy": occ})

        print(res)
        totCos1 = costModel.objects.filter(
            date__gte=str(fromYear)+"-"+fromMonth).filter(date__lte=str(toYear)+"-"+toMonth).aggregate(Sum('amount'))['amount__sum']

        totCos2 = costExpenseModel.objects.filter(
            date__gte=str(fromYear)+"-"+fromMonth).filter(date__lte=str(toYear)+"-"+toMonth).aggregate(Sum('amount'))['amount__sum']
        if not totCos1:
            totCos1 = 0
        if not totCos2:
            totCos2 = 0
        # totCos = totCos1+totCos2
        profit = totInc - totCos1

        return render(request,  "tax.html", {"plot": plot, "capExp": totCos2, "occupancy": round((tD/356)*100, 1), "totPro": profit, "totCos": totCos1, "totInc": totInc, "type": 1, "tomonth": toMonth, "frommonth": fromMonth, "toyear": toYear,  "fromyear": fromYear, "all_reserve": res, "settings": settings, "page_name": "Tax summary", "name": user[0].name})



# @csrf_exempt
# def taxView(request):
#     sessionId = request.COOKIES.get("session_id_$cedar")
#     if not sessionId:
#         return HttpResponseRedirect('/')
#     settings = settingsModel.objects.all()[0]
#     sess = sessionModel.objects.filter(token=sessionId)
#     # print("user--",sess)
#     user = adminModel.objects.filter(
#         email=sess[0].email)

#     year = request.GET.get("year")
#     month = request.GET.get("month")

#     if year == None or month == None:
#         allReserve = []

#     else:
#         year = int(year)
#         month = int(month)
#         d_fmt = "{0:>02}.{1:>02}.{2}"
#         date_from = datetime.strptime(
#             d_fmt.format(1, month, year), '%d.%m.%Y').date()
#         last_day_of_month = calendar.monthrange(year, month)[1]
#         date_to = datetime.strptime(
#             d_fmt.format(last_day_of_month, month, year), '%d.%m.%Y').date()
#         allReserve = list(reservationModel.objects.filter(
#             Q(checkInDate__gte=date_from)
#             &
#             Q(checkInDate__lte=date_to)).values())

#         # allReserve = costSerializer(allReserve, many=True).data

#     return render(request,  "tax.html", {"year": year, "month": month, "all_reserve": allReserve, "settings": settings, "page_name": "Tax", "name": user[0].name})
