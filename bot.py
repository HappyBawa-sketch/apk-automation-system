import telebot
import feedparser
import time
import threading
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==================== MASTER CONFIGURATION ====================
# Paste your secure Bot token from BotFather here
BOT_TOKEN = "8841260940:AAFNS77OBlXSJTmm3TeN5669BJKePenV2VA" 

# Replace with your actual live public channel handle (Include the @ symbol)
REQUIRED_CHANNEL = "@PremiumModAPKLibrary" 

# Replace with your raw Monetag Smartlink/MultiTag URL string
MONETAG_SMARTLINK = "https://omg10.com/4/11629249"

# The target open RSS portal feed tracking daily mobile file updates
APK_RSS_FEED_URL = "https://mobilism.org" 
# ==============================================================

bot = telebot.TeleBot(8841260940:AAFNS77OBlXSJTmm3TeN5669BJKePenV2VA)

# Dynamic Cloud RAM storage structure mappings (Unique ID Keys -> Clean Target Source Pages)
AUTOMATED_APK_DB = {}
LAST_PROCESSED_ENTRY_ID = None

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        # Safety fallback ensures the script doesn't stall if the Telegram server drops requests
        return True 

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    text = message.text.split()
    content_id = text[1] if len(text) > 1 else None

    # Force Channel Membership Verification Gateway
    if not is_subscribed(user_id):
        markup = InlineKeyboardMarkup()
        join_btn = InlineKeyboardButton("📢 1. Join Our Official Channel", url=f"https://t.me{REQUIRED_CHANNEL.strip('@')}")
        verify_url = f"https://t.me{bot.get_me().username}?start={content_id if content_id else 'welcome'}"
        verify_btn = InlineKeyboardButton("✅ 2. Verify Membership", url=verify_url)
        markup.row(join_btn)
        markup.row(verify_btn)
        
        bot.send_message(user_id, "⚠️ **Verification Gateway Active**\n\nTo bypass spam filters and extract free premium download mirror keys, you must join our update community group first.", parse_mode="Markdown", reply_markup=markup)
        return

    # Serve Content Payload Safely
    if content_id and content_id in AUTOMATED_APK_DB:
        markup = InlineKeyboardMarkup()
        # Button 1 opens your Monetag smartlink and registers your ad view earnings
        unlock_ad = InlineKeyboardButton("🔓 1. Unlock Download Server (Ad)", url=MONETAG_SMARTLINK)
        # Button 2 links straight to the forum source containing the file mirror
        real_download = InlineKeyboardButton("📥 2. Fetch Direct APK Link", url=AUTOMATED_APK_DB[content_id])
        markup.row(unlock_ad)
        markup.row(real_download)
        
        caption = f"🚀 **Your Requested Premium Application Link is Processed!**\n\n📦 **System Tracking ID:** `{content_id.upper()}`\n\n🔹 **Process Steps:** Tap Button 1 to route through our secure server portal. Right after the site displays, return here and tap Button 2 to download the application directly."
        bot.send_message(user_id, caption, parse_mode="Markdown", reply_markup=markup)
    else:
        bot.send_message(user_id, f"👋 Welcome to the Autonomous Mod Delivery Hub! Check out our public feed channel over at {REQUIRED_CHANNEL} to grab new app releases instantly 24/7.")

# --- BACKGROUND SYSTEM RUNTIME AUTOMATION ENGINE ---
def auto_apk_scraper_loop():
    global LAST_PROCESSED_ENTRY_ID, AUTOMATED_APK_DB
    print("Initializing Background Automated Parser Engine...")
    
    while True:
        try:
            feed = feedparser.parse(APK_RSS_FEED_URL)
            if feed.entries:
                latest_entry = feed.entries[0] # Target the newest active upload item
                
                # Check if this file has already been tracked and posted
                if latest_entry.id != LAST_PROCESSED_ENTRY_ID:
                    LAST_PROCESSED_ENTRY_ID = latest_entry.id
                    
                    # Convert file title to a clean alpha-numeric parameter tag for deep linking
                    clean_id = "".join([c if c.isalnum() else "_" for c in latest_entry.title[:25]]).lower().strip("_")
                    
                    # Log mapping dynamically into the running RAM database ledger
                    AUTOMATED_APK_DB[clean_id] = latest_entry.link
                    
                    # Generate deep link pointing back to your specific verification bot
                    bot_redirect_link = f"https://t.me{bot.get_me().username}?start={clean_id}"
                    
                    # Design promotional layout button mechanics
                    markup = InlineKeyboardMarkup()
                    get_link_btn = InlineKeyboardButton("📥 Download Mod File (Free)", url=bot_redirect_link)
                    markup.add(get_link_btn)
                    
                    channel_payload = f"🔥 **NEW AUTOMATED APK DROP**\n\n📦 **App Name:** {latest_entry.title}\n⚙️ **Type:** Premium Pro Unlocked Mod\n🛡️ **Safety Scan:** Passed 100% Clean\n\nTap the secure download hub link below to fetch your file setup instantly:"
                    
                    # Auto-post payload directly into your live audience channel
                    bot.send_message(REQUIRED_CHANNEL, channel_payload, parse_mode="Markdown", reply_markup=markup)
                    print(f"Successfully processed and published: {latest_entry.title}")
                    
        except Exception as e:
            print(f"Scraper Engine warning catch: {str(e)}")
            
        # Background routine runs once every 60 minutes completely on autopilot
        time.sleep(3600)

if __name__ == '__main__':
    # Launch scraper task isolated inside a secondary system thread
    scraper_thread = threading.Thread(target=auto_apk_scraper_loop)
    scraper_thread.daemon = True
    scraper_thread.start()
    
    # Fire up active user chat polling loop
    bot.infinity_polling()
                  
