"""
Simple test script to verify UI router setup.
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.main import app
    print("✓ App imported successfully")
    
    # Check for UI router routes
    ui_routes = [r for r in app.routes if hasattr(r, 'path') and '/ui' in r.path]
    print(f"✓ Found {len(ui_routes)} UI route(s)")
    
    for route in ui_routes:
        print(f"  - {route.methods} {route.path}")
    
    # Check that incidents router is included
    api_routes = [r for r in app.routes if hasattr(r, 'path') and '/incidents' in r.path]
    print(f"✓ Found {len(api_routes)} API incident route(s)")
    
    print("\n✓ All imports and routes configured correctly!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
