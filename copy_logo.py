import shutil

source_image = r"C:\Users\Mahmoud\.gemini\antigravity-ide\brain\afc1cce0-ff63-406a-9068-38acadfdf1c1\job_market_analysis_logo_1779578513688.png"
destination_image = "logo.png"

try:
    shutil.copyfile(source_image, destination_image)
    print("✅ Logo copied successfully to logo.png!")
except Exception as e:
    print(f"❌ Error copying logo: {e}")
