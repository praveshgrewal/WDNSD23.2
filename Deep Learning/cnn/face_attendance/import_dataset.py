import os
import shutil
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'face_attendance.settings')
django.setup()

from attendance.models import Employee

def import_existing_dataset():
    dataset_src = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataset'))
    
    if not os.path.exists(dataset_src):
        print(f"Source dataset directory not found at: {dataset_src}")
        return

    print(f"Found source dataset directory: {dataset_src}")
    
    # Names of directories to import
    folders = ['piyush', 'pravesh_grewal']
    
    for folder in folders:
        src_path = os.path.join(dataset_src, folder)
        if not os.path.exists(src_path):
            print(f"Folder not found: {src_path}")
            continue
            
        # Clean name for presentation
        display_name = folder.replace('_', ' ').title()
        email = f"{folder.lower()}@example.com"
        
        # Create or update employee
        employee, created = Employee.objects.get_or_create(
            email=email,
            defaults={
                'name': display_name,
                'department': 'Development'
            }
        )
        
        if created:
            print(f"Created new employee: {display_name}")
        else:
            print(f"Found existing employee: {display_name}")
            
        # Get target directory for faces
        target_dir = employee.get_faces_dir()
        
        # Clear existing faces in target directory to avoid mixing up
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        os.makedirs(target_dir, exist_ok=True)
        
        # Copy images
        copied_count = 0
        for filename in os.listdir(src_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                src_file = os.path.join(src_path, filename)
                # Save with proper padded names
                dest_file = os.path.join(target_dir, f"face_{copied_count+1:04d}.jpg")
                shutil.copy2(src_file, dest_file)
                copied_count += 1
                
        # Update images_count and is_trained (we will train the CNN model later)
        employee.images_count = copied_count
        employee.is_trained = False  # Mark as false until CNN is run
        employee.save()
        
        print(f"Successfully copied {copied_count} images for {display_name} to {target_dir}")

if __name__ == '__main__':
    import_existing_dataset()
