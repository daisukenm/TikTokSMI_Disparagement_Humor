from tiktok_api import TikTokAPIClient
from tiktok_api.io import get_video_ids, video_data_to_csv, comments_data_to_csv
from dotenv import load_dotenv
import random
import os

load_dotenv()

# Data Storage Area
Storage_Area = os.environ["DATA_STORAGE"]

# username list
username_list = ["aaronparnas1", "briantylercohen", "davidpakmanshow", "harryjsisson", "joyreidofficial", "mattxiv", "philipdefranco", "rbreich", "tizzyent", "underthedesknews", "adamcalhoun1", "danbongino", "candaceoshow", "daterightstuff", "patrickbetdavid", "real.benshapiro", "the_jefferymead", "thecharliekirkshow", "thecommentssection", "theofficertatum", "tuckercarlson"]

# Data range
# The end_date must be no more than 30 days after the start_date.
# You should run the code twice: 20241001-20241031 and 20241101-20241130
start_date = "20241001"
end_date = "20241130"

comment_data_batch = "batch_1" # change batch number every time you run the code

# Directories
video_dir = os.path.join(Storage_Area, "video_data")
comments_dir = os.path.join(Storage_Area, "comments_data", comment_data_batch)
video_csv_dir = os.path.join(Storage_Area, f"{start_date}_{end_date}_video_data.csv")
comments_csv_dir = os.path.join(Storage_Area, "comments_data", f"{start_date}_{end_date}_comments_data_{comment_data_batch}.csv")

# Authenticate
client = TikTokAPIClient(
    client_key=os.environ['TIKTOK_KEY'],
    client_secret=os.environ['TIKTOK_SECRET']
)

# custom function dealing with API daily limit
def get_already_fetched_video_comments(comment_data_path):
    """
    Extract video IDs of which comment data is already fetched by previous API call.
    """
    filelist = []
    for file in os.listdir(comment_data_path):
        if file.endswith(".json"):
            video_id = file.replace("_comments.json", "")
            try:
                video_id = int(video_id)
                filelist.append(video_id)
            except Exception:
                pass
    return filelist

# Fetch video data
for username in username_list:
    client.fetch_video_data(username, start_date, end_date, mode="username", output_dir=video_dir)

# Convert video json data to csv
video_data_to_csv(video_dir, output_file=video_csv_dir)

# Fetch comments for each video
# This chunk will most likely run out the API daily limit
video_ids = get_video_ids(video_dir)
already_fetched_video_comments = get_already_fetched_video_comments(comments_dir)

print(f"Total: {len(video_ids)}, Already done: {len(already_fetched_video_comments)}, What is left: {len(video_ids) - len(already_fetched_video_comments)}")

remaining_videos = [vid for vid in video_ids if vid not in already_fetched_video_comments]
random.shuffle(remaining_videos) # shuffle so that you get random videos
for vid in remaining_videos:
    client.fetch_comments_data(vid, output_dir=comments_dir)

# Convert comments JSONs to CSV
comments_data_to_csv(comments_dir, video_data_path=video_dir, output_file=comments_csv_dir)
