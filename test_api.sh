#!/bin/bash

# Test script for iLearning API Gateway
# Run this after: docker compose up --build

BASE_URL="http://localhost:8080"
DIRECT_URL="http://localhost:8000"

echo "=============================================="
echo "  iLearning API Gateway Test Script"
echo "=============================================="
echo ""

# 1. Test NGINX health endpoint
echo "1. Testing NGINX health endpoint..."
echo "   GET $BASE_URL/healthz"
curl -s "$BASE_URL/healthz"
echo ""
echo ""

# 2. Test backend root (via gateway)
echo "2. Testing backend root via gateway..."
echo "   GET $BASE_URL/api/"
# Note: FastAPI root is at / not /api/, so this may 404
# Let's try the direct backend root instead
curl -s "$DIRECT_URL/"
echo ""
echo ""

# 3. Test /api/upload with a sample text file
echo "3. Testing /api/upload (via gateway)..."
echo "   POST $BASE_URL/api/upload"
echo "   Creating sample.txt..."
echo "The mitochondria is the powerhouse of the cell. It produces ATP through cellular respiration." > /tmp/sample.txt
UPLOAD_RESULT=$(curl -s -X POST "$BASE_URL/api/upload" \
  -F "file=@/tmp/sample.txt")
echo "   Response: $UPLOAD_RESULT"
echo ""

# Extract text from upload result for next tests
EXTRACTED_TEXT=$(echo "$UPLOAD_RESULT" | grep -o '"text":"[^"]*"' | cut -d'"' -f4)
if [ -z "$EXTRACTED_TEXT" ]; then
  EXTRACTED_TEXT="The mitochondria is the powerhouse of the cell."
fi
echo ""

# 4. Test /api/generate (essay mode)
echo "4. Testing /api/generate (essay mode, via gateway)..."
echo "   POST $BASE_URL/api/generate"
GENERATE_RESULT=$(curl -s -X POST "$BASE_URL/api/generate" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"$EXTRACTED_TEXT\", \"mode\": \"essay\"}")
echo "   Response (truncated): ${GENERATE_RESULT:0:300}..."
echo ""
echo ""

# 5. Test /api/generate (mcq mode)
echo "5. Testing /api/generate (MCQ mode, via gateway)..."
echo "   POST $BASE_URL/api/generate"
MCQ_RESULT=$(curl -s -X POST "$BASE_URL/api/generate" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"$EXTRACTED_TEXT\", \"mode\": \"mcq\"}")
echo "   Response (truncated): ${MCQ_RESULT:0:300}..."
echo ""
echo ""

# 6. Test /api/chat
echo "6. Testing /api/chat (via gateway)..."
echo "   POST $BASE_URL/api/chat"
CHAT_RESULT=$(curl -s -X POST "$BASE_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"$EXTRACTED_TEXT\", \"history\": [], \"question\": \"What is the main function of mitochondria?\"}")
echo "   Response (truncated): ${CHAT_RESULT:0:300}..."
echo ""
echo ""

# 7. Test /api/grade (essay mode) - simplified
echo "7. Testing /api/grade (essay mode, via gateway)..."
echo "   POST $BASE_URL/api/grade"
GRADE_RESULT=$(curl -s -X POST "$BASE_URL/api/grade" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"$EXTRACTED_TEXT\", \"mode\": \"essay\", \"user_answer\": \"The mitochondria produces energy for the cell through ATP synthesis.\", \"generated\": \"Write an essay about cellular respiration.\"}")
echo "   Response (truncated): ${GRADE_RESULT:0:300}..."
echo ""
echo ""

# 8. Check FastAPI docs availability
echo "8. Checking FastAPI docs availability..."
echo "   Via gateway: $BASE_URL/docs"
DOCS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/docs")
echo "   Status: $DOCS_STATUS"
echo ""

echo "=============================================="
echo "  Test Complete!"
echo "=============================================="
echo ""
echo "Gateway URL:  $BASE_URL/api/..."
echo "Direct URL:   $DIRECT_URL/api/..."
echo "Swagger Docs: $BASE_URL/docs (via gateway)"
echo "              $DIRECT_URL/docs (direct)"
echo ""

# Cleanup
rm -f /tmp/sample.txt
