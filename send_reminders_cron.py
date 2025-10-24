#!/usr/bin/env python
"""
Cron job script for sending daily follow-up reminders.

Usage:
    python send_reminders_cron.py

Schedule with cron (Linux/Mac):
    # Run daily at 9 AM
    0 9 * * * cd /path/to/job-tracker && /path/to/venv/bin/python send_reminders_cron.py

Schedule with Task Scheduler (Windows):
    1. Open Task Scheduler
    2. Create Basic Task
    3. Set trigger: Daily at 9:00 AM
    4. Action: Start a program
    5. Program: C:\path\to\venv\Scripts\python.exe
    6. Arguments: send_reminders_cron.py
    7. Start in: C:\path\to\job-tracker

Schedule with Render Cron Jobs:
    Add to render.yaml:
    - type: cron
      name: daily-reminders
      schedule: "0 9 * * *"
      command: python send_reminders_cron.py

Schedule with GitHub Actions:
    See .github/workflows/daily-reminders.yml
"""

import sys
import os
from datetime import datetime

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.scheduler import send_daily_reminders

if __name__ == '__main__':
    print(f"Starting daily reminders at {datetime.now()}")
    print("-" * 60)
    
    try:
        result = send_daily_reminders()
        
        print("\n" + "=" * 60)
        print("REMINDER SUMMARY")
        print("=" * 60)
        print(f"Date: {result['date']}")
        print(f"Total applications checked: {result['total_applications']}")
        print(f"Reminders sent: {result['sent']}")
        print(f"Failed: {result['failed']}")
        print("=" * 60)
        
        # Exit with error code if all failed
        if result['total_applications'] > 0 and result['sent'] == 0:
            print("\nERROR: No reminders were sent successfully!")
            sys.exit(1)
        
        print("\n✓ Reminder job completed successfully")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
