#!/bin/bash
# Financial Incident Replay System - Deployment Verification Script
# This script verifies that all necessary components are in place

echo "🔍 Financial Incident Replay System - Deployment Verification"
echo "=============================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counter
TOTAL=0
PASSED=0

# Function to check if file/directory exists
check_exists() {
    local path="$1"
    local description="$2"
    ((TOTAL++))
    
    if [ -e "$path" ]; then
        echo -e "${GREEN}✓${NC} $description"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $description (missing: $path)"
    fi
}

# Function to check if file contains string
check_contains() {
    local file="$1"
    local string="$2"
    local description="$3"
    ((TOTAL++))
    
    if grep -q "$string" "$file" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $description"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $description"
    fi
}

echo "📁 Backend Files"
echo "=================="
check_exists "backend/app/main.py" "FastAPI main application"
check_exists "backend/app/ai" "AI integration module"
check_exists "backend/app/api" "API routes"
check_exists "backend/requirements.txt" "Python dependencies"
check_exists "backend/.env" "Backend configuration"
check_contains "backend/.env" "AI_ENABLED" "AI_ENABLED setting"
check_contains "backend/.env" "ANTHROPIC_API_KEY" "Anthropic API key"
check_contains "backend/requirements.txt" "fastapi" "FastAPI dependency"
check_contains "backend/requirements.txt" "sqlalchemy" "SQLAlchemy dependency"

echo ""
echo "⚛️  Frontend Files"
echo "=================="
check_exists "ui/app/page.tsx" "Home page"
check_exists "ui/app/incidents/page.tsx" "Dashboard page"
check_exists "ui/app/incidents/\[id\]/page.tsx" "Incident detail page"
check_exists "ui/lib/api.ts" "API client"
check_exists "ui/components/StatusBadge.tsx" "StatusBadge component"
check_exists "ui/components/ConfidenceBar.tsx" "ConfidenceBar component"
check_exists "ui/components/AnalysisSection.tsx" "AnalysisSection component"
check_exists "ui/components/IncidentCard.tsx" "IncidentCard component"
check_exists "ui/components/CreateIncidentModal.tsx" "CreateIncidentModal component"
check_exists "ui/package.json" "Frontend package.json"
check_contains "ui/package.json" "lucide-react" "lucide-react dependency"
check_contains "ui/package.json" "\"next\"" "Next.js dependency"
check_contains "ui/package.json" "\"react\"" "React dependency"

echo ""
echo "📚 Documentation Files"
echo "====================="
check_exists "QUICK_START_COMPLETE.md" "Quick start guide"
check_exists "FRONTEND_SETUP.md" "Frontend setup guide"
check_exists "PROJECT_DELIVERY_SUMMARY.md" "Project delivery summary"

echo ""
echo "🔧 Configuration Files"
echo "====================="
check_exists "ui/tsconfig.json" "TypeScript config"
check_exists "ui/tailwind.config.ts" "Tailwind config"
check_exists "ui/next.config.ts" "Next.js config"

echo ""
echo "📊 Summary"
echo "=========="
echo "Files/Configs verified: $PASSED / $TOTAL"
echo ""

if [ $PASSED -eq $TOTAL ]; then
    echo -e "${GREEN}✓ All components present and configured!${NC}"
    echo ""
    echo "🚀 Next steps:"
    echo "1. Backend: python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"
    echo "2. Frontend: cd ui && npm install && npm run dev"
    echo "3. Browser: http://localhost:3000"
    exit 0
else
    echo -e "${YELLOW}⚠  Some components missing or misconfigured${NC}"
    echo "Please check the errors above and run setup again"
    exit 1
fi
