from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Repair

ALL_STATUSES = ['Принято', 'В работе', 'Готово', 'Выдано']

def dashboard(request):
    repairs = Repair.objects.all().order_by('-accepted_at')

    # Создание нового заказа
    if request.method == "POST" and "create_repair" in request.POST:
        client_name = request.POST.get("client_name", "").strip()
        client_phone = request.POST.get("client_phone", "").strip()
        device_model = request.POST.get("device_model", "").strip()
        issue_description = request.POST.get("issue_description", "").strip()
        custom_id = request.POST.get("custom_id", "").strip()

        data = {
            "client_name": client_name,
            "client_phone": client_phone,
            "device_model": device_model,
            "issue_description": issue_description,
        }
        if custom_id:
            data["id"] = custom_id

        Repair.objects.create(**data)
        return redirect('dashboard')

    # Фильтры
    q = request.GET.get('q', '').strip()
    client = request.GET.get('client', '').strip()
    device = request.GET.get('device', '').strip()
    selected_statuses = request.GET.getlist('status')
    period = request.GET.get('period', 'all')

    if q:
        repairs = repairs.filter(id__icontains=q)
    if client:
        repairs = repairs.filter(client_name__icontains=client)
    if device:
        repairs = repairs.filter(device_model__icontains=device)

    if selected_statuses:
        repairs = repairs.filter(status__in=selected_statuses)
    elif 'filter_applied' in request.GET:
        repairs = repairs.none()

    now = timezone.now()
    if period == 'today':
        repairs = repairs.filter(accepted_at__date=now.date())
    elif period == 'week':
        repairs = repairs.filter(accepted_at__gte=now - timedelta(days=7))
    elif period == 'month':
        repairs = repairs.filter(accepted_at__gte=now - timedelta(days=30))

    context = {
        'repairs': repairs,
        'all_statuses': ALL_STATUSES,
        'selected_statuses': selected_statuses if selected_statuses or 'filter_applied' in request.GET else ALL_STATUSES,
        'period': period,
        'q': q,
        'client': client,
        'device': device,
    }
    return render(request, 'repairs/dashboard.html', context)

def repair_detail(request, pk):
    repair = get_object_or_404(Repair, pk=pk)

    if request.method == "POST":
        repair.status = request.POST.get("status", repair.status)
        repair.completed_works = request.POST.get("completed_works", "")
        try:
            repair.cost = float(request.POST.get("cost", 0) or 0)
        except ValueError:
            repair.cost = 0.0
        repair.save()
        return redirect('repair_detail', pk=repair.pk)

    return render(request, 'repairs/detail.html', {'repair': repair})
