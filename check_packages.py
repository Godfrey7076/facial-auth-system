try:
    import django
    print(f"✓ Django: {django.__version__}")
except ImportError:
    print("✗ Django: NOT INSTALLED")

try:
    import rest_framework
    print("✓ Django REST Framework: INSTALLED")
except ImportError:
    print("✗ Django REST Framework: NOT INSTALLED")

try:
    import numpy
    print(f"✓ NumPy: {numpy.__version__}")
except ImportError:
    print("✗ NumPy: NOT INSTALLED")

try:
    import cv2
    print(f"✓ OpenCV: {cv2.__version__}")
except ImportError:
    print("✗ OpenCV: NOT INSTALLED")

try:
    import sklearn
    print(f"✓ scikit-learn: {sklearn.__version__}")
except ImportError:
    print("✗ scikit-learn: NOT INSTALLED")

try:
    from PIL import Image
    print("✓ Pillow: INSTALLED")
except ImportError:
    print("✗ Pillow: NOT INSTALLED")

try:
    import django_filters
    print("✓ Django Filter: INSTALLED")
except ImportError:
    print("✗ Django Filter: NOT INSTALLED")

try:
    import corsheaders
    print("✓ Django CORS Headers: INSTALLED")
except ImportError:
    print("✗ Django CORS Headers: NOT INSTALLED")
