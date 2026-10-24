import time
import random
import os
import sys

# ANSI Colors
GREEN = '\033[92m'
BLUE = '\033[94m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RED = '\033[91m'
MAGENTA = '\033[95m'
WHITE = '\033[0m'
BOLD = '\033[1m'

def clear():
    os.system('clear')

def type_print(text, color=WHITE, speed=0.02):
    sys.stdout.write(color)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    sys.stdout.write(WHITE + '\n')

def fake_loading(text, duration=2.0):
    sys.stdout.write(YELLOW + text + " ")
    sys.stdout.flush()
    steps = 20
    for _ in range(steps):
        sys.stdout.write("█")
        sys.stdout.flush()
        time.sleep(duration/steps)
    sys.stdout.write(GREEN + " [DONE]\n" + WHITE)
    sys.stdout.flush()

clear()

# Intro
type_print("=====================================================", CYAN, 0.01)
type_print("      🩸 BEINGHUMAN BLOOD - VERCEL DEPLOYMENT CLI 🩸", BOLD + RED, 0.02)
type_print("=====================================================", CYAN, 0.01)
time.sleep(0.5)

type_print("[SYSTEM] Initializing environment...", MAGENTA, 0.02)
fake_loading("Loading modules...", 1.5)
fake_loading("Connecting to Firebase Firestore...", 2.0)

print("\n" + WHITE + "----------------- BUILD LOGS -----------------" + WHITE + "\n")

# Huge list of fake coding lines
fake_lines = [
    "npm install firebase-admin --save",
    "git add .",
    "git commit -m 'Fixed notification click handler'",
    "git push origin main",
    "const app = initializeApp(firebaseConfig);",
    "import { getFirestore } from 'firebase/firestore';",
    "await db.collection('donors').where('blood', '==', currentReqBlood).get();",
    "messaging.getToken({ vapidKey: VAPID_KEY })",
    "fetch('/api/send-notification', { method: 'POST', body: payload })",
    "Compiling src/components/Home.jsx...",
    "Optimizing images and fonts...",
    "Running linter and fixing auto-correctable errors...",
    "API Route: /api/send-notification initialized",
    "Fetching active FCM tokens from database...",
    "Total tokens found: 4",
    "Sending payload to Firebase Cloud Messaging...",
    "Response Status: 200 OK",
    "Notification Delivered to Device: cX9...",
    "Firestore reads: 150 / 50,000",
    "Firestore writes: 12 / 20,000",
    "Latency: 18ms - Connection Secure 🔒",
    "Building production bundle...",
    "Vercel CLI: Deploying to production...",
    "Uploading static assets...",
    "Edge Network: Cache updated in 24 regions",
    "Running security audit on rules...",
    "Warning: Service Worker cache needs update.",
    "Clearing cache for domain beinghumanblood.vercel.app...",
    "Resolving DNS for api.vercel.com...",
    "Checking Firebase Auth state persistence...",
    "Refreshing user session token...",
]

# Random highlights
highlights = [
    "[SYSTEM] 🩸 BeingHuman Core Module Loaded Successfully...",
    "[INFO] Real-time listener established on Firestore...",
    "[SUCCESS] Admin Dashboard authorization verified.",
    "[SYSTEM] Push Notification payload accepted by Google.",
    "[INFO] Donor matched: Blood B+, City Daska."
]

print("\n")

# Run loop for 35 seconds
start_time = time.time()
while time.time() - start_time < 35:
    # Randomly pick a line and color
    line = random.choice(fake_lines)
    color = random.choice([GREEN, BLUE, CYAN, YELLOW])
    
    # Random speed to simulate typing
    speed = random.uniform(0.005, 0.03)
    
    # Print the line
    type_print("> " + line, color, speed)
    
    # Occasionally print a highlight
    if random.random() < 0.15:
        type_print(random.choice(highlights), RED, 0.03)
        
    # Occasional fake progress bar
    if random.random() < 0.08:
        fake_loading("Processing...", 1.0)

# Final Success Message
print("\n")
time.sleep(1)
type_print("=====================================================", GREEN, 0.01)
type_print(" ✅ BUILD SUCCESSFUL - DEPLOYMENT LIVE ON VERCEL!", BOLD + GREEN, 0.04)
type_print("=====================================================", GREEN, 0.01)
print("\n")
