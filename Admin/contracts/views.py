from django.http import JsonResponse

def metrics_summary(request):
    data = {
        "ok": True,
        "users_total": 0,
        "offers_total": 0,
        "timestamp": request.META.get("REQUEST_TIME_FLOAT", None),
    }
    return JsonResponse(data)
