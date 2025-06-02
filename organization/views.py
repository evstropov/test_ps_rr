from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from organization.models import Organization


@require_http_methods(["GET"])
def organization_balance(request, inn: int):
    try:
        organization = Organization.objects.values('tin', 'wallet__balance').get(tin=inn)
    except Organization.DoesNotExist:
        return JsonResponse({"error": "Organization not found"}, status=404)
    else:
        return JsonResponse({"inn": organization['tin'], "balance": organization['wallet__balance']})
