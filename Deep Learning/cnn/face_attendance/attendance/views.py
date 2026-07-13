"""
Views for the Face Attendance application.
Handles dashboard, user management, face capture, training, and attendance marking.
"""
import json
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Count, Q

from .models import Employee, Attendance
from .forms import EmployeeForm
from .face_utils import (
    detect_faces, extract_face, decode_image_from_base64,
    save_face_image, FACE_SIZE
)


def dashboard(request):
    """Main dashboard view showing attendance overview."""
    today = timezone.now().date()

    total_employees = Employee.objects.count()
    trained_employees = Employee.objects.filter(is_trained=True).count()

    today_attendance = Attendance.objects.filter(date=today)
    checked_in = today_attendance.filter(status='IN').count()
    checked_out = today_attendance.filter(status='OUT').count()

    recent_attendance = Attendance.objects.select_related('employee')[:10]
    employees = Employee.objects.all()[:6]

    context = {
        'total_employees': total_employees,
        'trained_employees': trained_employees,
        'checked_in': checked_in,
        'checked_out': checked_out,
        'recent_attendance': recent_attendance,
        'employees': employees,
        'today': today,
    }
    return render(request, 'attendance/dashboard.html', context)


def add_user(request):
    """View to register a new employee."""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            return redirect('capture_faces', employee_id=employee.employee_id)
    else:
        form = EmployeeForm()

    return render(request, 'attendance/add_user.html', {'form': form})


def capture_faces(request, employee_id):
    """View for webcam face capture page."""
    employee = get_object_or_404(Employee, employee_id=employee_id)
    return render(request, 'attendance/capture.html', {
        'employee': employee,
        'min_images': 200,
    })


@csrf_exempt
@require_POST
def capture_frame(request, employee_id):
    """
    AJAX endpoint to receive a webcam frame, detect face, and save it.
    Expects JSON body with 'image' key containing base64-encoded image.
    """
    employee = get_object_or_404(Employee, employee_id=employee_id)

    try:
        data = json.loads(request.body)
        base64_image = data.get('image', '')

        if not base64_image:
            return JsonResponse({'success': False, 'error': 'No image data received'})

        # Decode the image
        image = decode_image_from_base64(base64_image)
        if image is None:
            return JsonResponse({'success': False, 'error': 'Failed to decode image'})

        # Detect faces
        faces = detect_faces(image)

        if len(faces) == 0:
            return JsonResponse({
                'success': False,
                'error': 'No face detected. Please position your face in the camera.',
                'face_detected': False
            })

        if len(faces) > 1:
            return JsonResponse({
                'success': False,
                'error': 'Multiple faces detected. Please ensure only one face is visible.',
                'face_detected': False
            })

        # Extract the face
        face = extract_face(image, faces[0])

        # Save the face image
        save_dir = employee.get_faces_dir()
        current_count = employee.images_count
        save_face_image(face, save_dir, current_count + 1)

        # Update count
        employee.images_count = current_count + 1
        employee.save(update_fields=['images_count'])

        # Get face coordinates for drawing on the frontend
        x, y, w, h = [int(v) for v in faces[0]]

        return JsonResponse({
            'success': True,
            'count': employee.images_count,
            'face_detected': True,
            'face_coords': {'x': x, 'y': y, 'w': w, 'h': h}
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def train_view(request):
    """View to trigger and display model training."""
    employees = Employee.objects.filter(images_count__gte=10)

    context = {
        'employees': employees,
        'total_images': sum(e.images_count for e in employees),
    }
    return render(request, 'attendance/train.html', context)


@csrf_exempt
@require_POST
def train_model_api(request):
    """AJAX endpoint to trigger model training."""
    try:
        from .train_model import train_model

        result = train_model()

        if result['success']:
            # Mark all employees with images as trained
            Employee.objects.filter(images_count__gte=10).update(is_trained=True)

        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def mark_attendance_view(request):
    """View for marking attendance via face recognition."""
    return render(request, 'attendance/mark_attendance.html')


@csrf_exempt
@require_POST
def recognize_face_api(request):
    """
    AJAX endpoint to recognize a face and mark attendance.
    Expects JSON body with 'image' key containing base64-encoded image.
    """
    try:
        data = json.loads(request.body)
        base64_image = data.get('image', '')

        if not base64_image:
            return JsonResponse({'success': False, 'error': 'No image data received'})

        # Decode the image
        image = decode_image_from_base64(base64_image)
        if image is None:
            return JsonResponse({'success': False, 'error': 'Failed to decode image'})

        # Detect faces
        faces = detect_faces(image)

        if len(faces) == 0:
            return JsonResponse({
                'success': False,
                'error': 'No face detected',
                'face_detected': False
            })

        # Extract the largest face
        largest_face = max(faces, key=lambda f: f[2] * f[3])
        face_image = extract_face(image, largest_face)

        # Recognize the face
        from .train_model import recognize_face
        result = recognize_face(face_image)

        if not result['recognized']:
            x, y, w, h = [int(v) for v in largest_face]
            return JsonResponse({
                'success': False,
                'error': result.get('error', 'Face not recognized'),
                'confidence': result.get('confidence', 0),
                'face_detected': True,
                'face_coords': {'x': x, 'y': y, 'w': w, 'h': h}
            })

        # Face recognized — mark attendance
        desired_action = data.get('desired_action')
        if desired_action not in ['IN', 'OUT']:
            return JsonResponse({
                'success': False,
                'error': 'Desired action must be Check In or Check Out.',
            })

        employee = get_object_or_404(Employee, employee_id=result['employee_id'])
        today = timezone.now().date()
        now = timezone.now()

        attendance = Attendance.objects.filter(employee=employee, date=today).first()

        if desired_action == 'IN':
            if attendance is None:
                attendance = Attendance.objects.create(
                    employee=employee,
                    date=today,
                    check_in=now,
                    status='IN',
                    confidence=result['confidence'],
                )
                action = 'CHECK IN'
            else:
                attendance.check_in = now
                attendance.status = 'IN'
                attendance.confidence = result['confidence']
                attendance.save(update_fields=['check_in', 'status', 'confidence'])
                action = 'CHECK IN (Updated)'
        else:
            if attendance is None:
                attendance = Attendance.objects.create(
                    employee=employee,
                    date=today,
                    check_out=now,
                    status='OUT',
                    confidence=result['confidence'],
                )
                action = 'CHECK OUT'
            else:
                previous_status = attendance.status
                attendance.check_out = now
                attendance.status = 'OUT'
                attendance.confidence = result['confidence']
                attendance.save(update_fields=['check_out', 'status', 'confidence'])
                action = 'CHECK OUT' if previous_status == 'IN' else 'CHECK OUT (Updated)'

        x, y, w, h = [int(v) for v in largest_face]

        return JsonResponse({
            'success': True,
            'employee_name': employee.name,
            'employee_id': employee.employee_id,
            'department': employee.department,
            'action': action,
            'confidence': result['confidence'],
            'time': now.strftime('%I:%M:%S %p'),
            'face_detected': True,
            'face_coords': {'x': x, 'y': y, 'w': w, 'h': h}
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_POST
def manual_attendance_api(request):
    """AJAX endpoint to manually check in/out an employee."""
    try:
        data = json.loads(request.body)
        employee_id = data.get('employee_id')
        email = data.get('email')

        if not employee_id and not email:
            return JsonResponse({'success': False, 'error': 'Employee ID or email is required.'})

        if employee_id:
            employee = get_object_or_404(Employee, employee_id=employee_id)
        else:
            employee = get_object_or_404(Employee, email=email)

        today = timezone.now().date()
        now = timezone.now()

        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=today,
            defaults={
                'check_in': now,
                'status': 'IN',
                'confidence': 0.0,
            }
        )

        if not created:
            if attendance.status == 'IN':
                attendance.check_out = now
                attendance.status = 'OUT'
                attendance.save(update_fields=['check_out', 'status'])
                action = 'CHECK OUT'
            else:
                attendance.check_out = now
                attendance.save(update_fields=['check_out'])
                action = 'CHECK OUT (Updated)'
        else:
            action = 'CHECK IN'

        return JsonResponse({
            'success': True,
            'employee_name': employee.name,
            'employee_id': employee.employee_id,
            'department': employee.department,
            'action': action,
            'confidence': 0.0,
            'time': now.strftime('%I:%M:%S %p'),
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def attendance_list(request):
    """View to display attendance records with filtering."""
    date_filter = request.GET.get('date', '')
    name_filter = request.GET.get('name', '')
    status_filter = request.GET.get('status', '')

    records = Attendance.objects.select_related('employee').all()

    if date_filter:
        records = records.filter(date=date_filter)

    if name_filter:
        records = records.filter(employee__name__icontains=name_filter)

    if status_filter:
        records = records.filter(status=status_filter)

    context = {
        'records': records[:100],
        'date_filter': date_filter,
        'name_filter': name_filter,
        'status_filter': status_filter,
    }
    return render(request, 'attendance/attendance_list.html', context)


def user_detail(request, employee_id):
    """View individual employee details and attendance history."""
    employee = get_object_or_404(Employee, employee_id=employee_id)
    records = Attendance.objects.filter(employee=employee).order_by('-date')[:30]

    context = {
        'employee': employee,
        'records': records,
        'total_days': records.count(),
    }
    return render(request, 'attendance/user_detail.html', context)


def user_list(request):
    """View to list all registered employees."""
    employees = Employee.objects.all()
    return render(request, 'attendance/user_list.html', {'employees': employees})
