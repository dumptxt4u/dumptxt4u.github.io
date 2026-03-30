#!/usr/bin/env python3
"""
WhatsApp + WhatsApp Business Status & Video Automatic Backup
Runs daily at 3:00 PM and 11:00 PM via cron
"""

import os
import zipfile
import sys
from datetime import datetime
import logging

# ====================== CONFIGURATION ======================
BASE_PATH = "/run/user/1000/gvfs/ftp:host=192.168.1.38,port=8080/Android/media"

WHATSAPP_STATUS_PATH = f"{BASE_PATH}/com.whatsapp/WhatsApp/Media/.Statuses"
WHATSAPP_VIDEO_PATH  = f"{BASE_PATH}/com.whatsapp/WhatsApp/Media/WhatsApp Video"

WHATSAPP_BUSINESS_STATUS_PATH = f"{BASE_PATH}/com.whatsapp.w4b/WhatsApp Business/Media/.Statuses"
WHATSAPP_BUSINESS_VIDEO_PATH  = f"{BASE_PATH}/com.whatsapp.w4b/WhatsApp Business/Media/WhatsApp Video"

BACKUP_DIR = os.path.expanduser("~/whatsapp_backups")   # Change if you want different location

# Create log file
LOG_FILE = os.path.join(BACKUP_DIR, "whatsapp_backup.log")

# ===========================================================

def setup_logging():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger().addHandler(console)

def zip_folder(source_folder, output_zip, folder_type="Media"):
    """Zip contents of folder. Returns number of files zipped."""
    if not os.path.exists(source_folder):
        logging.warning(f"Folder not found: {source_folder}")
        return 0

    files = [f for f in os.listdir(source_folder) 
             if os.path.isfile(os.path.join(source_folder, f))]

    if not files:
        logging.info(f"No files found in {folder_type} folder")
        return 0

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            file_path = os.path.join(source_folder, file)
            arcname = os.path.basename(file_path)
            zipf.write(file_path, arcname)

    logging.info(f"✓ {folder_type}: {len(files)} files → {os.path.basename(output_zip)}")
    return len(files)

def main():
    setup_logging()
    logging.info("="*60)
    logging.info("Starting WhatsApp Status + Video Backup")
    logging.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create dated subfolders for better organization
    today = datetime.now().strftime("%Y-%m-%d")
    whatsapp_dir = os.path.join(BACKUP_DIR, "whatsapp", today)
    business_dir = os.path.join(BACKUP_DIR, "whatsappbusiness", today)
    
    os.makedirs(whatsapp_dir, exist_ok=True)
    os.makedirs(business_dir, exist_ok=True)

    total_files = 0

    try:
        # === WhatsApp Regular ===
        logging.info("Backing up WhatsApp...")
        status_zip = os.path.join(whatsapp_dir, f"whatsapp_statuses_{timestamp}.zip")
        video_zip  = os.path.join(whatsapp_dir, f"whatsapp_videos_{timestamp}.zip")

        count1 = zip_folder(WHATSAPP_STATUS_PATH, status_zip, "Statuses")
        count2 = zip_folder(WHATSAPP_VIDEO_PATH, video_zip, "Videos")
        total_files += count1 + count2

        # === WhatsApp Business ===
        logging.info("Backing up WhatsApp Business...")
        b_status_zip = os.path.join(business_dir, f"whatsappbusiness_statuses_{timestamp}.zip")
        b_video_zip  = os.path.join(business_dir, f"whatsappbusiness_videos_{timestamp}.zip")

        count3 = zip_folder(WHATSAPP_BUSINESS_STATUS_PATH, b_status_zip, "Statuses")
        count4 = zip_folder(WHATSAPP_BUSINESS_VIDEO_PATH, b_video_zip, "Videos")
        total_files += count3 + count4

        logging.info(f"Backup completed successfully! Total files backed up: {total_files}")

    except Exception as e:
        logging.error(f"Backup failed: {str(e)}", exc_info=True)
        sys.exit(1)

    logging.info("Script finished.\n")

if __name__ == "__main__":
    main()
